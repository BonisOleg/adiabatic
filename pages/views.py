from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import get_language
from django.urls import reverse
from .models import Page, Hero, Partner


def home_redirect(request):
    """Редирект з кореня на головну сторінку"""
    return HttpResponseRedirect(reverse('pages:home'))


def test_view(request):
    """Тестовий view без шаблону"""
    return HttpResponse("""
    <h1>🎉 Django працює!</h1>
    <p>Це простий тестовий view без шаблону.</p>
    <ul>
        <li><a href="/">Повернутися на головну</a></li>
        <li><a href="/?debug=1">Debug режим</a></li>
        <li><a href="/about/">Про компанію</a></li>
        <li><a href="/catalog/">Каталог</a></li>
    </ul>
    """)


def home(request):
    """Головна сторінка"""
    # Тимчасове рішення для тестування
    if request.GET.get('debug'):
        return HttpResponse("<h1>Debug: Django працює!</h1><p>Проблема в шаблоні або контексті.</p>")
    
    try:
        page = Page.objects.get(page_type='home', is_published=True)
    except Page.DoesNotExist:
        page = None
    
    try:
        # Отримуємо тільки активні hero секції з зображеннями
        heroes = Hero.objects.filter(is_active=True).exclude(background_image='').order_by('order')
    except Exception:
        heroes = []
    
    try:
        # Отримуємо тільки активних партнерів
        partners = Partner.objects.filter(is_published=True).order_by('order')
    except Exception:
        partners = []
    
    context = {
        'page': page,
        'heroes': heroes,
        'partners': partners,
    }
    return render(request, 'pages/home.html', context)


def about(request):
    """Сторінка про компанію"""
    try:
        page = Page.objects.get(page_type='about', is_published=True)
    except Page.DoesNotExist:
        page = None
    
    context = {
        'page': page,
    }
    return render(request, 'pages/about.html', context)


def contacts(request):
    """Сторінка контактів"""
    try:
        page = Page.objects.get(page_type='contacts', is_published=True)
    except Page.DoesNotExist:
        page = None
    
    context = {
        'page': page,
    }
    return render(request, 'pages/contacts.html', context)





def page_detail(request, slug):
    """Детальна сторінка за slug"""
    page = get_object_or_404(Page, slug=slug, is_published=True)
    
    context = {
        'page': page,
    }
    return render(request, 'pages/page_detail.html', context)
