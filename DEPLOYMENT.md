# 🚀 Деплоймент Django проекту Adiabatic на Render.com

## 📋 Підготовка проекту

### ✅ Файли для деплойменту (вже створені):

1. **`requirements.txt`** - Python залежності з PostgreSQL підтримкою
2. **`Procfile`** - Команда запуску для Render
3. **`render.yaml`** - Автоматична конфігурація Render
4. **`build.sh`** - Скрипт збірки (міграції, статичні файли)
5. **`.gitignore`** - Виключення файлів з Git
6. **`env_production_example.txt`** - Приклад змінних середовища

## 🔧 Кроки деплойменту

### 1. ✅ Git репозиторій вже готовий!

Проект вже підключений до GitHub: `git@github.com:BonisOleg/adiabatic.git`

**Статус**: ✅ Код успішно завантажено в репозиторій

### 2. Створення аккаунту на Render.com

1. Перейдіть на [render.com](https://render.com)
2. Зареєструйтеся або увійдіть
3. Підключіть ваш GitHub/GitLab аккаунт

### 3. Створення PostgreSQL бази даних

1. На dashboard Render натисніть **"New"** → **"PostgreSQL"**
2. Заповніть форму:
   - **Name**: `adiabatic-db`
   - **Database**: `adiabatic`
   - **User**: `adiabatic_user`
   - **Region**: оберіть найближчий регіон
   - **Plan**: `Free` (для тестування)
3. Натисніть **"Create Database"**
4. **Збережіть External Database URL** - він знадобиться

### 4. Створення Web Service

#### 🎯 **Варіант A: Автоматично через Blueprint (РЕКОМЕНДУЄТЬСЯ!)**
1. На dashboard натисніть **"New"** → **"Blueprint"**
2. Підключіть ваш Git репозиторій: `git@github.com:BonisOleg/adiabatic.git`
3. Render автоматично знайде `render.yaml` та створить:
   - ✅ PostgreSQL базу даних `adiabatic-db`
   - ✅ Web Service `adiabatic-django`
   - ✅ Всі необхідні змінні середовища
   - ✅ Автоматичний деплоймент

**Переваги Blueprint**: Все налаштовується автоматично за 1 клік!

#### Варіант B: Ручне створення
1. На dashboard натисніть **"New"** → **"Web Service"**
2. Підключіть ваш Git репозиторій
3. Заповніть налаштування:
   - **Name**: `adiabatic-django`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn adiabatic.wsgi:application`
   - **Plan**: `Free`

### 5. Налаштування змінних середовища

#### 🎯 **При використанні Blueprint (автоматично):**
Всі змінні середовища налаштовуються автоматично з `render.yaml`:
- ✅ `SECRET_KEY` - генерується автоматично
- ✅ `DATABASE_URL` - підключається з PostgreSQL бази
- ✅ `DEBUG = False` - для продакшену
- ✅ `ALLOWED_HOSTS` - ваш домен Render
- ✅ `CSRF_TRUSTED_ORIGINS` - HTTPS домен

#### 📝 **При ручному створенні:**
В налаштуваннях вашого Web Service додайте:

#### Обов'язкові змінні:
```
SECRET_KEY = [згенерується автоматично або вставте свій]
DEBUG = False
DATABASE_URL = [скопіюйте з PostgreSQL бази даних]
ALLOWED_HOSTS = adiabatic-django.onrender.com
CSRF_TRUSTED_ORIGINS = https://adiabatic-django.onrender.com
```

#### Опціональні змінні:
```
REDIS_URL = redis://red-xxxxx:6379
SITE_URL = https://adiabatic-django.onrender.com
EMAIL_BACKEND = django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_HOST_USER = your-email@gmail.com
EMAIL_HOST_PASSWORD = your-app-password
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = noreply@adiabatic.com
```

### 6. Деплоймент

#### 🎯 **При використанні Blueprint:**
1. Після створення Blueprint Render автоматично почне деплоймент
2. Процес збірки включає:
   - ✅ Встановлення залежностей (`pip install -r requirements.txt`)
   - ✅ Збірка статичних файлів (`collectstatic`)
   - ✅ Виконання міграцій (`migrate`)
   - ✅ Ініціалізація базових даних (`setup_data`)

#### 📝 **При ручному створенні:**
1. Натисніть **"Deploy Latest Commit"** або **"Create Web Service"**
2. Render почне процес збірки з `build.sh`

### 7. Перевірка деплойменту

1. Дочекайтеся завершення деплойменту (5-10 хвилин)
2. Відкрийте ваш сайт: `https://adiabatic-django.onrender.com`
3. Перевірте адмінку: `https://adiabatic-django.onrender.com/admin/`

#### 🔑 **Дані для входу в адмінку:**
- **Логін**: `admin`
- **Пароль**: `admin123`

**Примітка**: Суперкористувач створюється автоматично при першому деплої через `setup_data` команду

## 🔍 Налагодження проблем

### Перегляд логів
```bash
# В Render dashboard перейдіть до вашого сервісу
# Натисніть "Logs" для перегляду логів в реальному часі
```

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

**Примітка**: При використанні Blueprint всі оновлення автоматично деплояться при push в `main` гілку

## 📊 Моніторинг

1. **Render Dashboard**: Перегляд статусу, логів, метрик
2. **Google Analytics**: Трафік сайту (якщо налаштовано)
3. **Error tracking**: Sentry або інші сервіси

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

## 🚀 **ШВИДКА ІНСТРУКЦІЯ ДЛЯ BLUEPRINT (5 ХВИЛИН)**

### 1. **Перейдіть на [render.com](https://render.com)**
### 2. **Натисніть "New" → "Blueprint"**
### 3. **Підключіть репозиторій**: `git@github.com:BonisOleg/adiabatic.git`
### 4. **Натисніть "Create Blueprint Instance"**
### 5. **Дочекайтеся завершення деплойменту (5-10 хв)**

**Все інше налаштовується автоматично!** 🎯

## 🔗 Корисні посилання

- [Render Documentation](https://render.com/docs)
- [Django Deployment Guide](https://docs.djangoproject.com/en/5.1/howto/deployment/)
- [PostgreSQL on Render](https://render.com/docs/databases)

---

**Проект готовий до деплойменту на Render.com через Blueprint!** 🎉
