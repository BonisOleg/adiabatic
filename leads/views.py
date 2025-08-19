from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import get_language
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
import json
import logging

from catalog.models import Product
from .models import Lead, LeadSource, LeadActivity
from .forms import LeadForm, QuickQuoteForm, ContactForm

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Отримати IP адресу клієнта"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_or_create_source(request):
    """Отримати або створити джерело заявки на основі UTM параметрів"""
    utm_source = request.GET.get('utm_source', '')
    utm_medium = request.GET.get('utm_medium', '')
    utm_campaign = request.GET.get('utm_campaign', '')
    
    if utm_source or utm_medium or utm_campaign:
        source_name = f"{utm_source}_{utm_medium}_{utm_campaign}".strip('_')
        source, created = LeadSource.objects.get_or_create(
            utm_source=utm_source,
            utm_medium=utm_medium,
            utm_campaign=utm_campaign,
            defaults={'name': source_name or 'Direct'}
        )
        return source
    
    # Створюємо джерело на основі реферера
    referrer = request.META.get('HTTP_REFERER', '')
    if 'google' in referrer.lower():
        source, created = LeadSource.objects.get_or_create(
            name='Google Organic',
            defaults={'utm_source': 'google', 'utm_medium': 'organic'}
        )
    elif 'facebook' in referrer.lower():
        source, created = LeadSource.objects.get_or_create(
            name='Facebook',
            defaults={'utm_source': 'facebook', 'utm_medium': 'social'}
        )
    else:
        source, created = LeadSource.objects.get_or_create(
            name='Direct',
            defaults={'utm_source': 'direct', 'utm_medium': 'none'}
        )
    
    return source


@require_http_methods(["POST"])
def submit_lead(request):
    """Основна функція відправки заявки (AJAX)"""
    try:
        # Парсимо JSON дані
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        # Отримуємо продукт якщо передано slug
        product = None
        product_slug = data.get('product_slug')
        if product_slug:
            try:
                product = Product.objects.get(slug=product_slug, is_published=True)
            except Product.DoesNotExist:
                pass
        
        # Створюємо форму
        form = LeadForm(data, product_slug=product_slug)
        
        if form.is_valid():
            # Зберігаємо заявку
            lead = form.save(commit=False)
            
            # Додаємо мета-дані
            lead.ip_address = get_client_ip(request)
            lead.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
            lead.language = get_language()
            lead.source = get_or_create_source(request)
            lead.source_page = request.META.get('HTTP_REFERER', '')[:500]
            lead.referrer = request.META.get('HTTP_REFERER', '')[:500]
            
            lead.save()
            
            # Створюємо активність
            LeadActivity.objects.create(
                lead=lead,
                activity_type='created',
                description=f'Заявка створена через форму на сайті',
                user='System'
            )
            
            # TODO: Відправляємо нотифікації (буде реалізовано пізніше)
            # send_lead_notifications.delay(lead.id)
            
            logger.info(f'Нова заявка створена: {lead.uuid} - {lead.email}')
            
            return JsonResponse({
                'success': True,
                'message': 'Дякуємо! Ваша заявка успішно відправлена.',
                'lead_uuid': str(lead.uuid),
                'redirect_url': f'/leads/thank-you/{lead.uuid}/'
            })
        else:
            # Повертаємо помилки валідації
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = [str(error) for error in field_errors]
            
            return JsonResponse({
                'success': False,
                'errors': errors,
                'message': 'Будь ласка, виправте помилки у формі.'
            })
    
    except Exception as e:
        logger.error(f'Помилка при створенні заявки: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': 'Виникла помилка при відправці заявки. Спробуйте пізніше.',
            'error': str(e) if settings.DEBUG else None
        })


@require_http_methods(["POST"])
def quick_quote(request):
    """Швидкий запит ціни (спрощена форма)"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        # Отримуємо продукт
        product = None
        product_id = data.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(id=product_id, is_published=True)
            except Product.DoesNotExist:
                pass
        
        form = QuickQuoteForm(data, product=product)
        
        if form.is_valid():
            lead = form.save(commit=False)
            
            # Додаємо мета-дані
            lead.ip_address = get_client_ip(request)
            lead.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
            lead.language = get_language()
            lead.source = get_or_create_source(request)
            lead.source_page = request.META.get('HTTP_REFERER', '')[:500]
            
            lead.save()
            
            # Створюємо активність
            LeadActivity.objects.create(
                lead=lead,
                activity_type='created',
                description=f'Швидкий запит ціни для продукту: {product.get_name() if product else "Загальний"}',
                user='System'
            )
            
            logger.info(f'Швидкий запит ціни: {lead.uuid} - {lead.email}')
            
            return JsonResponse({
                'success': True,
                'message': 'Дякуємо! Ми зв\'яжемося з вами найближчим часом.',
                'lead_uuid': str(lead.uuid)
            })
        else:
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = [str(error) for error in field_errors]
            
            return JsonResponse({
                'success': False,
                'errors': errors,
                'message': 'Будь ласка, заповніть всі обов\'язкові поля.'
            })
    
    except Exception as e:
        logger.error(f'Помилка при швидкому запиті: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': 'Виникла помилка. Спробуйте пізніше.'
        })


@require_http_methods(["POST"])
def contact(request):
    """Загальна контактна форма"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        form = ContactForm(data)
        
        if form.is_valid():
            lead = form.save(commit=False)
            
            # Додаємо мета-дані
            lead.ip_address = get_client_ip(request)
            lead.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
            lead.language = get_language()
            lead.source = get_or_create_source(request)
            lead.source_page = request.META.get('HTTP_REFERER', '')[:500]
            
            lead.save()
            
            # Створюємо активність
            LeadActivity.objects.create(
                lead=lead,
                activity_type='created',
                description='Заявка через контактну форму',
                user='System'
            )
            
            logger.info(f'Контактна заявка: {lead.uuid} - {lead.email}')
            
            return JsonResponse({
                'success': True,
                'message': 'Дякуємо за звернення! Ми відповімо вам найближчим часом.',
                'lead_uuid': str(lead.uuid)
            })
        else:
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = [str(error) for error in field_errors]
            
            return JsonResponse({
                'success': False,
                'errors': errors,
                'message': 'Будь ласка, виправте помилки у формі.'
            })
    
    except Exception as e:
        logger.error(f'Помилка в контактній формі: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': 'Виникла помилка. Спробуйте пізніше.'
        })


def thank_you(request):
    """Загальна сторінка подяки"""
    context = {
        'page_title': 'Дякуємо за заявку!',
    }
    return render(request, 'leads/thank_you.html', context)


def lead_form(request):
    """Сторінка з формою заявки"""
    context = {
        'page_title': 'Залишити заявку',
    }
    return render(request, 'leads/lead_form.html', context)


def thank_you_detail(request, lead_uuid):
    """Персоналізована сторінка подяки"""
    lead = get_object_or_404(Lead, uuid=lead_uuid)
    
    context = {
        'page_title': 'Дякуємо за заявку!',
        'lead': lead,
    }
    return render(request, 'leads/thank_you_detail.html', context)
