# Plan.md - Детальний план Django проекту Adiabatic

## 🎯 Огляд проекту

**Назва компанії:** Adiabatic  
**Тип проекту:** Корпоративний веб-сайт  
**Стек:** Django 5.1.3 + PostgreSQL + HTML/CSS/JS + Redis  
**Мови:** Українська, Російська, Англійська  

## 📋 Функціональні вимоги

### 1. Основний функціонал
- ✅ Адаптивний дизайн (мобільний/планшет/ПК)
- ✅ Мультимовність (i18n) - 3 мови
- ✅ 10 сторінок продуктової лінійки
- ✅ Система форм заявок з нотифікаціями
- ✅ SEO оптимізація
- ✅ Безпека (HTTPS, CSRF, XSS захист)
- ✅ Аналітика (GA4, custom events)

### 2. Спеціальний функціонал
- ✅ Платіжні посилання через Monobank Acquiring
- ✅ QR коди для документів з можливістю друку
- ✅ Інтеграція з пошта/Telegram/Viber
- ✅ Керування контентом через адмінку

## 🏗️ Архітектура проекту

### Django додатки

#### 1. `core` - Основні налаштування
```
core/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── views.py
├── urls.py
├── middleware.py     # Безпека, мови
├── context_processors.py
├── templatetags/
│   └── core_tags.py
└── migrations/
```

**Функції:**
- Базові налаштування проекту
- Мультимовність (LocaleMiddleware)
- Хедери безпеки
- Контекст процесори для глобальних даних
- 404/500 сторінки

#### 2. `pages` - Статичні сторінки
```
pages/
├── __init__.py
├── admin.py
├── apps.py
├── models.py        # Page, Section, Hero
├── views.py
├── urls.py
├── forms.py
└── migrations/
```

**Моделі:**
- `Page` - основні сторінки (Головна, Про компанію, Контакти)
- `Section` - секції сторінок (JSON конструктор)
- `Hero` - герой секції
- `Partner` - партнери компанії

#### 3. `catalog` - Продуктовий каталог
```
catalog/
├── __init__.py
├── admin.py
├── apps.py
├── models.py        # Category, Product, Spec, Gallery
├── views.py
├── urls.py
├── forms.py
├── services.py      # Бізнес логіка
└── migrations/
```

**Моделі:**
- `Category` - категорії продуктів
- `Product` - продукти (10 основних)
- `ProductSpec` - технічні характеристики
- `ProductGallery` - галерея зображень
- `ProductAdvantage` - переваги продукту
- `ProductDocument` - документи/сертифікати

#### 4. `leads` - Система заявок
```
leads/
├── __init__.py
├── admin.py
├── apps.py
├── models.py        # Lead, LeadSource, EmailTemplate
├── views.py
├── urls.py
├── forms.py
├── services.py      # Email, Telegram, Viber сервіси
├── tasks.py         # Celery tasks
└── migrations/
```

**Моделі:**
- `Lead` - заявки клієнтів
- `LeadSource` - джерела заявок
- `EmailTemplate` - шаблони листів
- `NotificationSettings` - налаштування нотифікацій

#### 5. `payment` - Платіжні посилання
```
payment/
├── __init__.py
├── admin.py
├── apps.py
├── models.py        # PaymentLink, PaymentSettings
├── views.py
├── urls.py
├── forms.py
├── services.py      # MonobankAcquiringService
├── webhooks.py      # Monobank webhook handler
├── templates/
│   └── payment/
├── static/
│   └── payment/
└── migrations/
```

**Моделі:**
- `PaymentLink` - платіжні посилання
- `PaymentSettings` - налаштування платіжної системи

#### 6. `documents` - QR документи
```
documents/
├── __init__.py
├── admin.py
├── apps.py
├── models.py        # Document, QRCode
├── views.py
├── urls.py
├── forms.py
├── services.py      # QR генератор, PDF обробка
├── utils.py         # PDF utilities
└── migrations/
```

**Моделі:**
- `Document` - документи компанії
- `QRCode` - QR коди для документів
- `DocumentAccess` - лог доступу до документів

#### 7. `analytics` - Аналітика
```
analytics/
├── __init__.py
├── admin.py
├── apps.py
├── models.py        # AnalyticsEvent, TrackingCode
├── views.py
├── services.py      # GA4, custom tracking
├── templatetags/
│   └── analytics_tags.py
└── migrations/
```

**Моделі:**
- `AnalyticsEvent` - кастомні події
- `TrackingCode` - коди відстеження
- `ConversionGoal` - цілі конверсій

## 🗄️ Структура бази даних

### Основні таблиці

#### Pages App
```sql
-- pages_page
id, slug, title_ua, title_ru, title_en, meta_description_ua, meta_description_ru, 
meta_description_en, is_published, created_at, updated_at

-- pages_section  
id, page_id, section_type, title, content (JSON), order, is_published

-- pages_partner
id, name, logo, website_url, order, is_published
```

#### Catalog App  
```sql
-- catalog_category
id, name_ua, name_ru, name_en, slug, description, icon, order, is_published

-- catalog_product
id, category_id, name_ua, name_ru, name_en, slug, short_description_ua, 
description_ua, hero_image, price_usd, is_featured, is_published

-- catalog_productspec
id, product_id, name_ua, name_ru, name_en, value, unit, order

-- catalog_productgallery
id, product_id, image, alt_text, order

-- catalog_productadvantage  
id, product_id, title_ua, title_ru, title_en, description, icon, order
```

#### Leads App
```sql
-- leads_lead
id, name, email, phone, message, product_id, source_page, status, 
consent_gdpr, ip_address, user_agent, created_at, processed_at

-- leads_leadsource
id, name, utm_source, utm_medium, utm_campaign, is_active

-- leads_notificationsettings
id, email_enabled, telegram_enabled, viber_enabled, telegram_chat_id, 
viber_token, smtp_settings (JSON)
```

#### Payment App
```sql
-- payment_paymentlink
id, unique_id (UUID), client_name, client_email, amount_usd, 
exchange_rate_usd_to_uah, final_amount_uah, description, status, 
duration_minutes, first_opened_at, expires_at, monobank_invoice_id

-- payment_paymentsettings  
id, company_name, description, default_contract_file, 
iban, recipient_name, recipient_code
```

#### Documents App
```sql
-- documents_document
id, title_ua, title_ru, title_en, file, document_type, is_public, 
qr_enabled, access_count, created_at

-- documents_qrcode
id, document_id, qr_uuid (UUID), qr_image, generated_pdf, is_active

-- documents_documentaccess
id, document_id, ip_address, user_agent, accessed_at, is_valid_qr
```

## 🌐 URL структура

### Мультимовні URL
```
/                    # Редірект на /ua/
/ua/                 # Українська версія
/ru/                 # Російська версія  
/en/                 # Англійська версія
```

### Основні сторінки
```
/{lang}/                          # Головна
/{lang}/about/                    # Про компанію
/{lang}/contacts/                 # Контакти
/{lang}/products/                 # Каталог продукції
/{lang}/products/{product-slug}/  # Сторінка продукту
```

### Спеціальні функції
```
/{lang}/leads/submit/             # Відправка заявки
/payment/pay/{uuid}/              # Сторінка оплати
/payment/webhook/monobank/        # Webhook Monobank
/documents/qr/{uuid}/             # Перегляд документа по QR
/documents/download/{doc-id}/     # Завантаження з QR
/admin/                          # Адмінка Django
```

## 📱 Responsive Breakpoints

```css
/* Mobile First Approach */
:root {
  --mobile: 360px;      /* iPhone SE */
  --mobile-lg: 576px;   /* Large phones */
  --tablet: 768px;      /* Tablets */
  --tablet-lg: 992px;   /* Large tablets */
  --desktop: 1200px;    /* Desktop */
  --desktop-xl: 1440px; /* Large desktop */
}
```

## 🔧 Технічні налаштування

### Безпека
- HTTPS обов'язково (Let's Encrypt)
- HSTS заголовки
- CSP (Content Security Policy)
- CSRF захист
- XSS захист
- Rate limiting для форм
- IP whitelist для адмінки

### SEO
- `robots.txt` та `sitemap.xml`
- Canonical URLs
- hreflang для мультимовності
- Open Graph / Twitter Cards
- Schema.org розмітка
- Lazy loading зображень
- WebP формат зображень

### Performance
- Redis кеш
- CSS/JS мінімізація
- Critical CSS
- Image optimization
- CDN (за потреби)
- Gunicorn + Nginx

### Мониторинг
- Health check endpoints
- Error tracking (Sentry опційно)
- Логування важливих подій
- Performance metrics

## 📦 Залежності (requirements.txt)

```txt
# Core Django
Django==5.1.3
psycopg2-binary==2.9.9
redis==5.0.1
celery[redis]==5.3.4

# Utilities
python-dotenv==1.0.1
Pillow==10.4.0
requests==2.32.3
qrcode[pil]==7.4.2

# i18n
django-modeltranslation==0.19.7

# Static files  
whitenoise==6.7.0

# Production
gunicorn==22.0.0

# Environment variables template
# Створити .env.example з повним списком змінних
```

## 🔧 Environment Variables (.env.example)

```bash
# Django Core
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/adiabatic_db

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Site URL
SITE_URL=https://yourdomain.com

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Monobank
MONOBANK_TOKEN=your-monobank-merchant-token

# Telegram
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-chat-id

# Viber
VIBER_BOT_TOKEN=your-viber-bot-token

# Analytics
GA4_MEASUREMENT_ID=G-XXXXXXXXXX
GOOGLE_ANALYTICS_PROPERTY_ID=your-property-id

# Security
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
```

## ⚙️ Django Settings.py (критичні налаштування)

```python
# Middleware порядок КРИТИЧНО ВАЖЛИВИЙ
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Для i18n
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Static files для Django 5.x
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Мови
LANGUAGES = [
    ('uk', 'Українська'),
    ('ru', 'Русский'),
    ('en', 'English'),
]
LANGUAGE_CODE = 'uk'
USE_I18N = True
USE_L10N = True

# Celery
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Kiev'
```

## 🚀 Деплоймент план

### 1. Розробка (Development)
- SQLite для швидкої розробки
- Django Development Server
- DEBUG=True

### 2. Продакшен (Production)  
- PostgreSQL база даних
- Redis для кешу та Celery
- Nginx + Gunicorn
- Let's Encrypt SSL
- Automated backup cron jobs

### 3. CI/CD Pipeline
```bash
# Локальна розробка
python manage.py runserver

# Тестування
python manage.py test
python manage.py check --deploy

# Деплоймент
git push origin main
# Автоматичний деплой через webhooks
```

## 🧪 Testing структура

```
tests/
├── __init__.py
├── test_models.py        # Тестування моделей
├── test_views.py         # Тестування views
├── test_forms.py         # Тестування форм
├── test_services.py      # Бізнес логіка
├── test_integrations.py  # Зовнішні сервіси
├── test_apis.py          # API endpoints
├── test_security.py      # Безпека
└── test_selenium.py      # E2E тести
```

## ✅ Чек-лист готовності

### Backend
- [ ] Django проект створено
- [ ] Всі додатки реалізовані
- [ ] Моделі та міграції готові
- [ ] API endpoints працюють
- [ ] Адмінка налаштована
- [ ] Тести написані

### Frontend  
- [ ] Responsive дизайн реалізовано
- [ ] Всі сторінки створені
- [ ] Форми працюють
- [ ] JavaScript функції готові
- [ ] Cross-browser тестування

### Інтеграції
- [ ] Email відправка працює
- [ ] Telegram/Viber інтеграція
- [ ] Monobank платежі
- [ ] QR коди генеруються
- [ ] Аналітика підключена

### Безпека та SEO
- [ ] HTTPS налаштовано
- [ ] Всі хедери безпеки
- [ ] SEO мета-теги
- [ ] Sitemap створено
- [ ] Performance оптимізовано

## 📋 Етапи розробки

### Етап 1: Базовий функціонал (2 тижні)
1. Django проект + віртуальне середовище
2. Базові додатки (core, pages)  
3. Мультимовність
4. Основні сторінки

### Етап 2: Каталог продукції (2 тижні)  
1. Додаток catalog
2. 10 сторінок продуктів
3. Адмінка для керування
4. Responsive дизайн

### Етап 3: Заявки та інтеграції (2 тижні)
1. Додаток leads
2. Email/Telegram/Viber
3. Celery для асинхронних задач
4. Rate limiting

### Етап 4: Платежі та документи (2 тижні)
1. Додаток payment (Monobank)
2. Додаток documents (QR коди)
3. PDF генерація
4. Тестування платежів

### Етап 5: SEO та продакшен (1 тиждень)
1. SEO оптимізація
2. Аналітика (GA4)
3. Продакшен налаштування  
4. Фінальне тестування

**Загальний термін: 9 тижнів**

## 💾 Backup стратегія

### Щоденні backup
- PostgreSQL dump
- Media files backup  
- `.env` файли (без секретів у git)

### Тижневі backup
- Повний системний backup
- Тестування відновлення
- Очищення старих backup

Цей план забезпечує повну реалізацію всіх вимог проекту з дотриманням найкращих практик Django розробки.
