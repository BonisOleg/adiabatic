# 🚀 Універсальний гід деплою Django проекту Adiabatic на Render.com

## 📋 Всі необхідні файли та налаштування

### 1. **requirements.txt** - Python залежності
```txt
# Core Django
Django==5.1.3
psycopg2-binary==2.9.9
redis==4.5.4
celery[redis]==5.3.4

# Database for Render
dj-database-url==2.1.0

# Utilities
python-dotenv==1.0.1
Pillow==11.3.0
requests==2.32.3
qrcode[pil]==7.4.2

# Static files  
whitenoise==6.7.0

# Production
gunicorn==22.0.0

# Testing
pytest==7.4.3
pytest-django==4.7.0
factory-boy==3.3.0
```

### 2. **Procfile** - Команда запуску
```procfile
web: gunicorn adiabatic.wsgi
```

### 3. **render.yaml** - Автоматична конфігурація Render
```yaml
services:
  - type: web
    name: adiabatic-django
    env: python
    plan: free
    buildCommand: |
      pip install -r requirements.txt
      python manage.py collectstatic --noinput
      python manage.py migrate
      python manage.py setup_data
    startCommand: gunicorn adiabatic.wsgi:application --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.9
      - key: DATABASE_URL
        fromDatabase:
          name: adiabatic-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: ALLOWED_HOSTS
        value: adiabatic-django.onrender.com,adiabatic-django-*.onrender.com
      - key: CSRF_TRUSTED_ORIGINS
        value: https://adiabatic-django.onrender.com,https://adiabatic-django-*.onrender.com
      - key: SITE_URL
        value: https://adiabatic-django.onrender.com
      - key: REDIS_URL
        value: redis://red-xxxxx:6379

databases:
  - name: adiabatic-db
    databaseName: adiabatic
    user: adiabatic_user
    plan: free
```

### 4. **build.sh** - Скрипт збірки
```bash
#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@adiabatic.com', 'admin123')" | python manage.py shell

# Setup initial data
python manage.py setup_data
```

### 5. **Налаштування Django (settings.py)** - Критичні частини
```python
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-k#*+d9^*ah_bt)rm3&83v%-^273c_20pc*(#gu+2yh(yy=_u4f')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')

# CSRF trusted origins for Render
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'https://localhost').split(',')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Database
# PostgreSQL for production, SQLite for development
if os.getenv('DATABASE_URL'):
    # Production database (PostgreSQL on Render)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Development database (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files для Django 5.x з whitenoise для Render
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Whitenoise налаштування для Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security Settings
if not DEBUG:
    # HTTPS налаштування для продакшену
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 рік
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

# Email Configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@adiabatic.com')
```

### 6. **Змінні середовища для продакшену**
```env
# Production Environment Variables для Render.com

# Django Core
DEBUG=False
SECRET_KEY=your-generated-secret-key-will-be-here
ALLOWED_HOSTS=adiabatic-django.onrender.com,adiabatic-django-*.onrender.com
CSRF_TRUSTED_ORIGINS=https://adiabatic-django.onrender.com,https://adiabatic-django-*.onrender.com

# Database (буде автоматично встановлено Render)
DATABASE_URL=postgresql://username:password@hostname:port/database

# Redis (опційно для Celery)
REDIS_URL=redis://hostname:port

# Site URL
SITE_URL=https://adiabatic-django.onrender.com

# Email Settings для продакшену
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@adiabatic.com

# Monobank (реальні дані для продакшену)
MONOBANK_TOKEN=your-real-monobank-token

# Telegram (реальні дані для продакшену)
TELEGRAM_BOT_TOKEN=your-real-telegram-bot-token
TELEGRAM_CHAT_ID=your-real-chat-id

# Viber (реальні дані для продакшену)
VIBER_BOT_TOKEN=your-real-viber-bot-token

# Analytics (реальні дані для продакшену)
GA4_MEASUREMENT_ID=G-XXXXXXXXXX
GOOGLE_ANALYTICS_PROPERTY_ID=your-property-id
```

## 🚀 ШВИДКА ІНСТРУКЦІЯ ДЕПЛОЮ (5 ХВИЛИН)

### Крок 1: Підготовка Git репозиторію
```bash
# Переконайтеся, що всі файли збережені
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Крок 2: Створення аккаунту на Render.com
1. Перейдіть на [render.com](https://render.com)
2. Зареєструйтеся або увійдіть
3. Підключіть ваш GitHub/GitLab аккаунт

### Крок 3: Деплой через Blueprint (РЕКОМЕНДУЄТЬСЯ!)
1. На dashboard натисніть **"New"** → **"Blueprint"**
2. Підключіть ваш Git репозиторій
3. Render автоматично знайде `render.yaml` та створить:
   - ✅ PostgreSQL базу даних `adiabatic-db`
   - ✅ Web Service `adiabatic-django`
   - ✅ Всі необхідні змінні середовища
   - ✅ Автоматичний деплоймент
4. Натисніть **"Create Blueprint Instance"**
5. Дочекайтеся завершення деплойменту (5-10 хвилин)

### Крок 4: Перевірка деплойменту
1. Відкрийте ваш сайт: `https://adiabatic-django.onrender.com`
2. Перевірте адмінку: `https://adiabatic-django.onrender.com/admin/`

#### 🔑 **Дані для входу в адмінку:**
- **Логін**: `admin`
- **Пароль**: `admin123`

## 🔧 Альтернативний ручний деплой

### Якщо Blueprint не працює:

#### 1. Створення PostgreSQL бази даних
1. На dashboard натисніть **"New"** → **"PostgreSQL"**
2. Заповніть форму:
   - **Name**: `adiabatic-db`
   - **Database**: `adiabatic`
   - **User**: `adiabatic_user`
   - **Region**: оберіть найближчий регіон
   - **Plan**: `Free`
3. Натисніть **"Create Database"**

#### 2. Створення Web Service
1. На dashboard натисніть **"New"** → **"Web Service"**
2. Підключіть ваш Git репозиторій
3. Заповніть налаштування:
   - **Name**: `adiabatic-django`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn adiabatic.wsgi:application`
   - **Plan**: `Free`

#### 3. Налаштування змінних середовища
```
SECRET_KEY = [згенерується автоматично]
DEBUG = False
DATABASE_URL = [скопіюйте з PostgreSQL бази даних]
ALLOWED_HOSTS = adiabatic-django.onrender.com
CSRF_TRUSTED_ORIGINS = https://adiabatic-django.onrender.com
```

## 🔍 Налагодження проблем

### Перегляд логів
- В Render dashboard перейдіть до вашого сервісу
- Натисніть "Logs" для перегляду логів в реальному часі

### Часті проблеми:

#### 1. Помилка міграцій
```bash
# Виконайте міграції вручну в Render Shell:
python manage.py migrate
```

#### 2. Статичні файли не завантажуються
```bash
# Перевірте збірку статичних файлів:
python manage.py collectstatic --noinput
```

#### 3. Помилка бази даних
- Перевірте правильність `DATABASE_URL`
- Переконайтеся, що PostgreSQL база створена

#### 4. ALLOWED_HOSTS помилка
- Додайте правильний домен в `ALLOWED_HOSTS`
- Перевірте `CSRF_TRUSTED_ORIGINS`

## 🚀 Оновлення проекту

Для оновлення деплойменту:
```bash
# Внесіть зміни в код
git add .
git commit -m "Update: your changes"
git push origin main

# Render автоматично перезапустить деплоймент
```

## 💰 Тарифні плани Render

- **Free Plan**: 
  - 750 годин на місяць
  - Засинає після 15 хвилин неактивності
  - 512MB RAM
  - Підходить для тестування

- **Starter Plan ($7/місяць)**:
  - Не засинає
  - 1GB RAM
  - Custom domains
  - Підходить для продакшену

## 📊 Моніторинг

1. **Render Dashboard**: Перегляд статусу, логів, метрик
2. **Google Analytics**: Трафік сайту (якщо налаштовано)
3. **Error tracking**: Sentry або інші сервіси

## 🔗 Корисні посилання

- [Render Documentation](https://render.com/docs)
- [Django Deployment Guide](https://docs.djangoproject.com/en/5.1/howto/deployment/)
- [PostgreSQL on Render](https://render.com/docs/databases)

---

## ✅ ЧЕКЛІСТ ГОТОВНОСТІ ДО ДЕПЛОЮ

- [ ] Всі файли конфігурації створені
- [ ] Git репозиторій оновлений
- [ ] Аккаунт на Render.com створений
- [ ] GitHub/GitLab підключений до Render
- [ ] Blueprint або ручне створення сервісів
- [ ] Деплоймент завершений
- [ ] Сайт працює
- [ ] Адмінка доступна
- [ ] Моніторинг налаштований

**Проект готовий до деплойменту на Render.com!** 🎉



