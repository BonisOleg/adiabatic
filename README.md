# Adiabatic - Корпоративний веб-сайт

## 🎯 Опис проекту

Корпоративний веб-сайт компанії Adiabatic, що спеціалізується на промисловому обладнанні та послугах. Сайт розроблений на Django з повною адаптивністю та мультимовністю.

## ✨ Основні функції

- 🌐 **Мультимовність**: Українська, Російська, Англійська
- 📱 **Адаптивний дизайн**: Мобільний, планшет, ПК
- 🏭 **Промислова тематика**: Стиль як promsteel.in.ua
- 📄 **10 сторінок продукції**: З технічними характеристиками
- 📝 **Форми заявок**: Інтеграція з email/Telegram/Viber
- 💳 **Платежі**: Monobank Acquiring
- 📊 **Аналітика**: GA4, Meta Pixel
- 🔒 **Безпека**: HTTPS, CSRF, XSS захист

## 🛠️ Технічний стек

- **Backend**: Django 5.1.3, Python 3.13
- **Database**: SQLite (розробка), PostgreSQL (продакшен)
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **Стилі**: CSS Variables, BEM методологія
- **Шрифти**: Inter, Montserrat
- **Адаптивність**: Mobile-first, iOS Safari оптимізація

## 🚀 Швидкий старт

### 1. Клонування репозиторію
```bash
git clone <repository-url>
cd PromNasos
```

### 2. Створення віртуального середовища
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# або
.venv\Scripts\activate  # Windows
```

### 3. Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 4. Налаштування змінних середовища
```bash
cp env_example.txt .env
# Відредагуйте .env файл з вашими налаштуваннями
```

### 5. Застосування міграцій
```bash
python manage.py migrate
```

### 6. Створення суперкористувача
```bash
python manage.py createsuperuser
```

### 7. Налаштування базових даних
```bash
python manage.py setup_data
```

### 8. Запуск сервера розробки
```bash
python manage.py runserver
```

Сайт буде доступний за адресою: http://localhost:8000

## 📁 Структура проекту

```
PromNasos/
├── adiabatic/          # Основні налаштування Django
├── core/              # Базові моделі та налаштування
├── pages/             # Основні сторінки сайту
├── catalog/           # Каталог продукції
├── leads/             # Форми заявок
├── payment/           # Платежі Monobank
├── documents/         # Документи та QR коди
├── analytics/         # Аналітика та метрики
├── templates/         # HTML шаблони
├── static/            # CSS, JS, зображення
├── media/             # Завантажені файли
├── locale/            # Файли перекладів
└── requirements.txt   # Залежності Python
```

## 🎨 Дизайн-система

### Кольорова палітра
- **Основний синій**: #1B365D (промисловий стиль)
- **Світліший синій**: #2E5984
- **Акцентний червоний**: #C4384D
- **Фіолетовий акцент**: #8B5FBF (з референсних зображень)

### Типографіка
- **Основні шрифти**: Inter, Montserrat
- **Розміри**: Від 12px до 72px (clamp для адаптивності)
- **Вага**: 300-800

### Компоненти
- **Кнопки**: Закруглені (border-radius: 50px)
- **Картки**: Тіні та hover ефекти
- **Hero секції**: Темний оверлей з білим текстом
- **Grid система**: CSS Grid з auto-fit

## 📱 Адаптивність

### Breakpoints
- **Mobile**: < 576px
- **Tablet**: 576px - 768px
- **Desktop**: > 768px

### iOS Safari оптимізація
- `-webkit-fill-available` для hero секцій
- Landscape орієнтація фікси
- Touch-friendly інтерактивні елементи

## 🌍 Мультимовність

### Підтримувані мови
- **Українська** (uk) - за замовчуванням
- **Російська** (ru)
- **Англійська** (en)

### URL структура
- `/uk/` - українська версія
- `/ru/` - російська версія
- `/en/` - англійська версія

## 🔧 Адміністративна панель

### Доступ
- URL: http://localhost:8000/admin/
- Логін: `admin`
- Пароль: `admin123`

### Моделі для керування
- **SiteSettings**: Глобальні налаштування сайту
- **Language**: Мови сайту
- **Menu**: Навігаційні меню
- **Page**: Основні сторінки
- **Hero**: Hero секції
- **Partner**: Партнери компанії

## 📊 SEO та аналітика

### SEO оптимізація
- Meta title/description для кожної сторінки
- Open Graph теги
- Hreflang для мультимовності
- Семантична HTML розмітка

### Аналітика
- Google Analytics 4
- Meta Pixel (Facebook)
- Custom events для форм та кліків

## 🚀 Деплоймент

### Розробка
- SQLite база даних
- Django Development Server
- DEBUG=True

### Продакшен
- PostgreSQL база даних
- Redis для кешу та Celery
- Nginx + Gunicorn
- Let's Encrypt SSL
- Backup стратегія

## 🧪 Тестування

```bash
# Запуск тестів
python manage.py test

# Перевірка безпеки
python manage.py check --deploy

# Перевірка стилю коду
python -m flake8
```

## 📝 Ліцензія

Цей проект розроблений для компанії Adiabatic.

## 🤝 Розробка

### Команди для розробки
```bash
# Створення міграцій
python manage.py makemigrations

# Застосування міграцій
python manage.py migrate

# Створення суперкористувача
python manage.py createsuperuser

# Запуск shell
python manage.py shell

# Збірка статичних файлів
python manage.py collectstatic
```

### Корисні посилання
- [Django Documentation](https://docs.djangoproject.com/)
- [Django i18n](https://docs.djangoproject.com/en/5.1/topics/i18n/)
- [CSS Variables](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [CSS Grid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout)

---

**Розроблено з ❤️ для Adiabatic**
