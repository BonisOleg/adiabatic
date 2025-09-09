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
            
            # Відправляємо нотифікації
            send_all_notifications(lead)
            
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


# Додано інтеграції (використовуючи наявні імпорти та стиль коду)
def send_telegram_notification(lead):
    """Відправка нотифікації в Telegram"""
    try:
        from .models import NotificationSettings
        import requests
        
        settings_obj = NotificationSettings.get_settings()
        
        if not settings_obj.telegram_enabled or not settings_obj.telegram_bot_token:
            return False
        
        message = f"""
🔔 *Нова заявка на сайті!*

👤 *Клієнт:* {lead.name}
📧 *Email:* {lead.email}
📱 *Телефон:* {lead.phone}

💼 *Компанія:* {lead.company or 'Не вказано'}
🎯 *Тип запиту:* {lead.get_inquiry_type_display()}

📝 *Повідомлення:*
{lead.message}

🌐 *Мова:* {lead.language}
📍 *IP:* {lead.ip_address}
🔗 *Джерело:* {lead.source.name if lead.source else 'Невідоме'}

⏰ *Час:* {lead.created_at.strftime('%d.%m.%Y %H:%M')}
        """
        
        url = f"https://api.telegram.org/bot{settings_obj.telegram_bot_token}/sendMessage"
        payload = {
            'chat_id': settings_obj.telegram_chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            # Створюємо активність
            LeadActivity.objects.create(
                lead=lead,
                activity_type='telegram_sent',
                description='Нотифікацію відправлено в Telegram',
                user='System'
            )
            logger.info(f'Telegram нотифікація відправлена для заявки {lead.uuid}')
            return True
        else:
            logger.error(f'Помилка Telegram API: {response.text}')
            return False
            
    except Exception as e:
        logger.error(f'Помилка відправки Telegram: {str(e)}')
        return False


def send_viber_notification(lead):
    """Відправка нотифікації в Viber"""
    try:
        from .models import NotificationSettings
        import requests
        
        settings_obj = NotificationSettings.get_settings()
        
        if not settings_obj.viber_enabled or not settings_obj.viber_bot_token:
            return False
        
        message = f"""
🔔 Нова заявка на сайті!

👤 Клієнт: {lead.name}
📧 Email: {lead.email}
📱 Телефон: {lead.phone}

💼 Компанія: {lead.company or 'Не вказано'}
🎯 Тип запиту: {lead.get_inquiry_type_display()}

📝 Повідомлення:
{lead.message}

🌐 Мова: {lead.language}
📍 IP: {lead.ip_address}
🔗 Джерело: {lead.source.name if lead.source else 'Невідоме'}

⏰ Час: {lead.created_at.strftime('%d.%m.%Y %H:%M')}
        """
        
        url = f"https://chatapi.viber.com/pa/send_message"
        headers = {
            'X-Viber-Auth-Token': settings_obj.viber_bot_token
        }
        payload = {
            'receiver': settings_obj.viber_admin_id,
            'type': 'text',
            'text': message
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            # Створюємо активність
            LeadActivity.objects.create(
                lead=lead,
                activity_type='viber_sent',
                description='Нотифікацію відправлено в Viber',
                user='System'
            )
            logger.info(f'Viber нотифікація відправлена для заявки {lead.uuid}')
            return True
        else:
            logger.error(f'Помилка Viber API: {response.text}')
            return False
            
    except Exception as e:
        logger.error(f'Помилка відправки Viber: {str(e)}')
        return False


def send_email_notification(lead):
    """Відправка email нотифікації"""
    try:
        from django.core.mail import send_mail
        from .models import NotificationSettings
        
        settings_obj = NotificationSettings.get_settings()
        
        if not settings_obj.email_enabled:
            return False
        
        subject = settings_obj.email_subject_template.format(name=lead.name)
        
        message = f"""
Нова заявка на сайті Adiabatic

Клієнт: {lead.name}
Email: {lead.email}
Телефон: {lead.phone}
Компанія: {lead.company or 'Не вказано'}

Тип запиту: {lead.get_inquiry_type_display()}

Повідомлення:
{lead.message}

Додаткова інформація:
- Мова: {lead.language}
- IP адреса: {lead.ip_address}
- Джерело: {lead.source.name if lead.source else 'Невідоме'}
- Дата створення: {lead.created_at.strftime('%d.%m.%Y %H:%M')}

Переглянути в адмінці: {settings.SITE_URL}/admin/leads/lead/{lead.id}/
        """
        
        recipients = [email.strip() for email in settings_obj.email_recipients.split(',')]
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False
        )
        
        # Створюємо активність
        LeadActivity.objects.create(
            lead=lead,
            activity_type='email_sent',
            description=f'Email відправлено на {", ".join(recipients)}',
            user='System'
        )
        
        logger.info(f'Email нотифікацію відправлено для заявки {lead.uuid}')
        return True
        
    except Exception as e:
        logger.error(f'Помилка відправки email: {str(e)}')
        return False


def send_all_notifications(lead):
    """Відправка всіх налаштованих нотифікацій"""
    results = {
        'email': send_email_notification(lead),
        'telegram': send_telegram_notification(lead),
        'viber': send_viber_notification(lead)
    }
    
    logger.info(f'Нотифікації для заявки {lead.uuid}: {results}')
    return results
