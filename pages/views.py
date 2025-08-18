from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import get_language
from django.urls import reverse
from .models import Page, Hero, Partner


def home_redirect(request):
    """Редирект з кореня на головну сторінку"""
    return HttpResponseRedirect(reverse('pages:home'))


def home(request):
    """Головна сторінка"""
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
