from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from catalog.models import Product
import uuid


class LeadSource(models.Model):
    """Джерела заявок для аналітики"""
    
    name = models.CharField(_('Назва джерела'), max_length=100)
    utm_source = models.CharField(_('UTM Source'), max_length=50, blank=True)
    utm_medium = models.CharField(_('UTM Medium'), max_length=50, blank=True)
    utm_campaign = models.CharField(_('UTM Campaign'), max_length=100, blank=True)
    is_active = models.BooleanField(_('Активне'), default=True)
    
    created_at = models.DateTimeField(_('Створено'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Джерело заявки')
        verbose_name_plural = _('Джерела заявок')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Lead(models.Model):
    """Заявки клієнтів"""
    
    STATUS_CHOICES = (
        ('new', _('Нова')),
        ('contacted', _('Зв\'язалися')),
        ('quote_sent', _('Відправили пропозицію')),
        ('closed_won', _('Закрито (продано)')),
        ('closed_lost', _('Закрито (втрачено)')),
        ('spam', _('Спам')),
    )
    
    INQUIRY_TYPES = (
        ('price_request', _('Запит ціни')),
        ('tech_consultation', _('Технічна консультація')),
        ('partnership', _('Партнерство')),
        ('service', _('Сервіс')),
        ('other', _('Інше')),
    )
    
    # Ідентифікація
    uuid = models.UUIDField(_('UUID'), default=uuid.uuid4, editable=False, unique=True)
    
    # Основна інформація
    name = models.CharField(_('Ім\'я'), max_length=100)
    email = models.EmailField(_('Email'))
    
    # Телефон з валідацією
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_('Номер телефону має бути у форматі: "+380501234567". До 15 цифр.')
    )
    phone = models.CharField(_('Телефон'), validators=[phone_regex], max_length=17)
    
    # Компанія (опційно)
    company = models.CharField(_('Компанія'), max_length=200, blank=True)
    position = models.CharField(_('Посада'), max_length=100, blank=True)
    
    # Деталі заявки
    inquiry_type = models.CharField(_('Тип запиту'), max_length=20, choices=INQUIRY_TYPES, default='price_request')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name=_('Продукт'), related_name='leads')
    subject = models.CharField(_('Тема'), max_length=200, blank=True)
    message = models.TextField(_('Повідомлення'))
    
    # Додаткові поля
    budget_range = models.CharField(_('Бюджет'), max_length=100, blank=True,
                                   help_text=_('Орієнтовний бюджет проекту'))
    project_timeline = models.CharField(_('Терміни проекту'), max_length=200, blank=True)
    
    # Мета-дані
    source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name=_('Джерело'))
    source_page = models.CharField(_('Сторінка джерела'), max_length=500, blank=True)
    referrer = models.CharField(_('Реферер'), max_length=500, blank=True)
    
    # Технічна інформація
    ip_address = models.GenericIPAddressField(_('IP адреса'), blank=True, null=True)
    user_agent = models.TextField(_('User Agent'), blank=True)
    language = models.CharField(_('Мова'), max_length=10, default='uk')
    
    # Статус
    status = models.CharField(_('Статус'), max_length=20, choices=STATUS_CHOICES, default='new')
    
    # GDPR
    consent_gdpr = models.BooleanField(_('Згода на обробку даних'), default=False)
    consent_marketing = models.BooleanField(_('Згода на маркетинг'), default=False)
    
    # Дати
    created_at = models.DateTimeField(_('Створено'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Оновлено'), auto_now=True)
    contacted_at = models.DateTimeField(_('Дата контакту'), blank=True, null=True)
    
    # Внутрішні примітки
    internal_notes = models.TextField(_('Внутрішні примітки'), blank=True,
                                     help_text=_('Примітки для команди (не видимі клієнту)'))
    
    class Meta:
        verbose_name = _('Заявка')
        verbose_name_plural = _('Заявки')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.email} ({self.get_status_display()})"
    
    def get_full_contact(self):
        """Повний контакт для відображення"""
        parts = [self.name]
        if self.company:
            parts.append(f"({self.company})")
        if self.position:
            parts.append(f"- {self.position}")
        return " ".join(parts)
    
    def get_short_message(self, length=100):
        """Скорочене повідомлення"""
        if len(self.message) <= length:
            return self.message
        return self.message[:length] + "..."


class NotificationSettings(models.Model):
    """Налаштування нотифікацій"""
    
    # Email налаштування
    email_enabled = models.BooleanField(_('Email увімкнено'), default=True)
    email_recipients = models.TextField(_('Email одержувачі'), 
                                       help_text=_('Email адреси через кому'),
                                       default='admin@adiabatic.com')
    email_subject_template = models.CharField(_('Шаблон теми email'), max_length=200,
                                             default='Нова заявка від {name}')
    
    # Telegram налаштування  
    telegram_enabled = models.BooleanField(_('Telegram увімкнено'), default=False)
    telegram_bot_token = models.CharField(_('Telegram Bot Token'), max_length=200, blank=True)
    telegram_chat_id = models.CharField(_('Telegram Chat ID'), max_length=50, blank=True)
    
    # Viber налаштування
    viber_enabled = models.BooleanField(_('Viber увімкнено'), default=False)
    viber_bot_token = models.CharField(_('Viber Bot Token'), max_length=200, blank=True)
    viber_admin_id = models.CharField(_('Viber Admin ID'), max_length=50, blank=True)
    
    # Інші налаштування
    notification_delay = models.PositiveIntegerField(_('Затримка нотифікації (сек)'), 
                                                    default=5,
                                                    help_text=_('Затримка перед відправкою'))
    max_retries = models.PositiveIntegerField(_('Максимум спроб'), default=3)
    
    created_at = models.DateTimeField(_('Створено'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Оновлено'), auto_now=True)
    
    class Meta:
        verbose_name = _('Налаштування нотифікацій')
        verbose_name_plural = _('Налаштування нотифікацій')
    
    def __str__(self):
        return f"Налаштування нотифікацій ({self.updated_at.strftime('%d.%m.%Y')})"
    
    @classmethod
    def get_settings(cls):
        """Отримати налаштування (singleton)"""
        settings, created = cls.objects.get_or_create(
            id=1,
            defaults={
                'email_enabled': True,
                'email_recipients': 'admin@adiabatic.com'
            }
        )
        return settings


class EmailTemplate(models.Model):
    """Шаблони email повідомлень"""
    
    TEMPLATE_TYPES = (
        ('new_lead', _('Нова заявка')),
        ('lead_confirmation', _('Підтвердження заявки')),
        ('quote_sent', _('Пропозиція відправлена')),
        ('follow_up', _('Нагадування')),
    )
    
    name = models.CharField(_('Назва шаблону'), max_length=100)
    template_type = models.CharField(_('Тип шаблону'), max_length=20, choices=TEMPLATE_TYPES)
    
    subject_uk = models.CharField(_('Тема (УК)'), max_length=200)
    subject_ru = models.CharField(_('Тема (РУ)'), max_length=200)
    subject_en = models.CharField(_('Тема (EN)'), max_length=200)
    
    content_uk = models.TextField(_('Контент (УК)'))
    content_ru = models.TextField(_('Контент (РУ)'))
    content_en = models.TextField(_('Контент (EN)'))
    
    is_active = models.BooleanField(_('Активний'), default=True)
    
    created_at = models.DateTimeField(_('Створено'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Оновлено'), auto_now=True)
    
    class Meta:
        verbose_name = _('Email шаблон')
        verbose_name_plural = _('Email шаблони')
        ordering = ['template_type', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
    
    def get_subject(self, language='uk'):
        """Отримати тему залежно від мови"""
        if language == 'ru':
            return self.subject_ru
        elif language == 'en':
            return self.subject_en
        return self.subject_uk
    
    def get_content(self, language='uk'):
        """Отримати контент залежно від мови"""
        if language == 'ru':
            return self.content_ru
        elif language == 'en':
            return self.content_en
        return self.content_uk


class LeadActivity(models.Model):
    """Журнал активності по заявці"""
    
    ACTIVITY_TYPES = (
        ('created', _('Створено')),
        ('email_sent', _('Email відправлено')),
        ('telegram_sent', _('Telegram відправлено')),
        ('viber_sent', _('Viber відправлено')),
        ('status_changed', _('Статус змінено')),
        ('contacted', _('Контакт здійснено')),
        ('note_added', _('Додано примітку')),
    )
    
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(_('Тип активності'), max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField(_('Опис'))
    user = models.CharField(_('Користувач'), max_length=100, blank=True)
    
    created_at = models.DateTimeField(_('Створено'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Активність заявки')
        verbose_name_plural = _('Активності заявок')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.lead.name} - {self.get_activity_type_display()}"
