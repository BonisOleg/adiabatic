from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import get_language
from django.urls import reverse
from .models import Page, Hero, Partner, Product


def get_page_or_none(page_type):
    """Допоміжна функція для отримання сторінки або None"""
    try:
        return Page.objects.get(page_type=page_type, is_published=True)
    except Page.DoesNotExist:
        return None


def get_partners():
    """Допоміжна функція для отримання партнерів"""
    try:
        return Partner.objects.filter(is_published=True).order_by('order')
    except Exception:
        return []


def home_redirect(request):
    """Редирект з кореня на головну сторінку"""
    return HttpResponseRedirect(reverse('pages:home'))


def home(request):
    """Головна сторінка"""
    page = get_page_or_none('home')
    
    try:
        # Отримуємо тільки активні hero секції з зображеннями
        heroes = Hero.objects.filter(is_active=True).exclude(background_image='').order_by('order')
    except Exception:
        heroes = []
    
    partners = get_partners()
    
    context = {
        'page': page,
        'heroes': heroes,
        'partners': partners,
    }
    return render(request, 'pages/home.html', context)


def about(request):
    """Сторінка про компанію"""
    context = {
        'page': get_page_or_none('about'),
    }
    return render(request, 'pages/about.html', context)


def contacts(request):
    """Сторінка контактів"""
    context = {
        'page': get_page_or_none('contacts'),
    }
    return render(request, 'pages/contacts.html', context)


def products(request):
    """Сторінка продуктів"""
    context = {
        'page': get_page_or_none('products'),
    }
    return render(request, 'pages/products.html', context)

def partners(request):
    """Сторінка партнерів"""
    context = {
        'page': get_page_or_none('partners'),
        'partners': get_partners(),
    }
    return render(request, 'pages/partners.html', context)


def blog(request):
    """Сторінка корисної інформації"""
    context = {
        'page': get_page_or_none('blog'),
    }
    return render(request, 'pages/blog.html', context)


def catalog(request):
    """Сторінка каталогу продукції"""
    products = Product.objects.filter(is_published=True).order_by('order')
    
    context = {
        'page': get_page_or_none('catalog'),
        'products': products,
    }
    return render(request, 'pages/catalog.html', context)


def page_detail(request, slug):
    """Детальна сторінка за slug"""
    page = get_object_or_404(Page, slug=slug, is_published=True)
    
    context = {
        'page': page,
    }
    return render(request, 'pages/page_detail.html', context)
