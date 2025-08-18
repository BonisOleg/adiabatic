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
    # Тимчасово повертаємо простий HTML без шаблонів
    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Adiabatic - Промислове обладнання</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .hero { background: linear-gradient(135deg, #0A2E6C, #6B46C1); color: white; padding: 60px 20px; text-align: center; border-radius: 12px; margin-bottom: 40px; }
            .hero h1 { font-size: 3rem; margin-bottom: 20px; }
            .hero p { font-size: 1.2rem; margin-bottom: 30px; }
            .btn { display: inline-block; padding: 12px 24px; background: #D62828; color: white; text-decoration: none; border-radius: 6px; margin: 0 10px; }
            .section { margin: 40px 0; }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }
            .feature { text-align: center; padding: 20px; background: #f5f5f5; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="hero">
            <h1>Adiabatic</h1>
            <p>Промислове обладнання та послуги. Надійні рішення для вашого бізнесу.</p>
            <a href="/catalog/" class="btn">Переглянути каталог</a>
            <a href="/about/" class="btn">Про компанію</a>
        </div>
        
        <div class="section">
            <h2>Наші переваги</h2>
            <div class="features">
                <div class="feature">
                    <h3>10+ років досвіду</h3>
                    <p>Багаторічний досвід у галузі промислового обладнання</p>
                </div>
                <div class="feature">
                    <h3>Якісне обладнання</h3>
                    <p>Тільки перевірені бренди та сертифіковане обладнання</p>
                </div>
                <div class="feature">
                    <h3>Повний сервіс</h3>
                    <p>Від консультації до монтажу та обслуговування</p>
                </div>
                <div class="feature">
                    <h3>24/7 підтримка</h3>
                    <p>Цілодобова технічна підтримка клієнтів</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>Контакти</h2>
            <p>📧 Email: info@adiabatic.com</p>
            <p>📞 Телефон: +380 44 123 45 67</p>
            <p>📍 Адреса: Київ, Україна</p>
        </div>
        
        <div class="section">
            <h2>Навігація</h2>
            <ul>
                <li><a href="/about/">Про компанію</a></li>
                <li><a href="/catalog/">Каталог продукції</a></li>
                <li><a href="/contacts/">Контакти</a></li>
                <li><a href="/admin/">Адмін панель</a></li>
            </ul>
        </div>
        
        <footer style="margin-top: 60px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; color: #666;">
            <p>&copy; 2025 Adiabatic. Всі права захищені.</p>
        </footer>
    </body>
    </html>
    """)


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
