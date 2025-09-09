from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    """Глобальні налаштування сайту"""
    site_name = models.CharField(_('Назва сайту'), max_length=100, default='Adiabatic')
    site_description = models.TextField(_('Опис сайту'), blank=True, max_length=500)
    contact_email = models.EmailField(_('Контактний email'), blank=True)
    contact_phone = models.CharField(_('Контактний телефон'), max_length=20, blank=True)
    address = models.TextField(_('Адреса'), blank=True, max_length=200)
    
    # SEO налаштування
    meta_title = models.CharField(_('Meta title'), max_length=60, blank=True)
    meta_description = models.TextField(_('Meta description'), max_length=160, blank=True)
    meta_keywords = models.CharField(_('Meta keywords'), max_length=255, blank=True)
    
    # Соціальні мережі
    facebook_url = models.URLField(_('Facebook URL'), blank=True)
    instagram_url = models.URLField(_('Instagram URL'), blank=True)
    linkedin_url = models.URLField(_('LinkedIn URL'), blank=True)
    
    # Аналітика
    google_analytics_id = models.CharField(_('Google Analytics ID'), max_length=20, blank=True)
    yandex_metrika_id = models.CharField(_('Yandex Metrika ID'), max_length=20, blank=True)
    
    created_at = models.DateTimeField(_('Створено'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Оновлено'), auto_now=True)
    
    class Meta:
        verbose_name = _('Налаштування сайту')
        verbose_name_plural = _('Налаштування сайту')
    
    def __str__(self):
        return self.site_name
    
    @classmethod
    def get_settings(cls):
        """Отримати налаштування сайту (створює якщо не існує)"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Language(models.Model):
    """Мови сайту"""
    code = models.CharField(_('Код мови'), max_length=5, unique=True)
    name = models.CharField(_('Назва мови'), max_length=50)
    name_local = models.CharField(_('Назва мови місцевою мовою'), max_length=50)
    is_active = models.BooleanField(_('Активна'), default=True)
    is_default = models.BooleanField(_('За замовчуванням'), default=False)
    flag = models.ImageField(_('Прапор'), upload_to='flags/', blank=True)
    
    class Meta:
        verbose_name = _('Мова')
        verbose_name_plural = _('Мови')
        ordering = ['-is_default', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def save(self, *args, **kwargs):
        if self.is_default:
            # Скидаємо всі інші мови як не за замовчуванням
            Language.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class Menu(models.Model):
    """Меню сайту"""
    MENU_TYPES = [
        ('header', _('Верхнє меню')),
        ('footer', _('Нижнє меню')),
        ('mobile', _('Мобільне меню')),
    ]
    
    name = models.CharField(_('Назва меню'), max_length=100)
    menu_type = models.CharField(_('Тип меню'), max_length=20, choices=MENU_TYPES)
    is_active = models.BooleanField(_('Активне'), default=True)
    
    class Meta:
        verbose_name = _('Меню')
        verbose_name_plural = _('Меню')
        ordering = ['menu_type', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_menu_type_display()})"


class MenuItem(models.Model):
    """Елементи меню"""
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items', verbose_name=_('Меню'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name=_('Батьківський елемент'))
    title = models.CharField(_('Заголовок'), max_length=100)
    url = models.CharField(_('URL'), max_length=200, blank=True)
    page = models.ForeignKey('pages.Page', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Сторінка'))
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    is_active = models.BooleanField(_('Активне'), default=True)
    is_external = models.BooleanField(_('Зовнішнє посилання'), default=False)
    open_in_new_tab = models.BooleanField(_('Відкривати в новій вкладці'), default=False)
    
    class Meta:
        verbose_name = _('Елемент меню')
        verbose_name_plural = _('Елементи меню')
        ordering = ['menu', 'order', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.menu.name})"
    
    def get_url(self):
        """Отримати URL для елемента меню"""
        if self.url:
            return self.url
        elif self.page:
            return self.page.get_absolute_url()
        return '#'


class PaymentSettings(models.Model):
    """Налаштування платіжної системи"""
    
    company_name = models.CharField(_('Назва компанії'), max_length=200)
    description = models.TextField(_('Опис'), blank=True)
    
    # Monobank налаштування
    monobank_token = models.CharField(_('Monobank Token'), max_length=200, blank=True)
    monobank_webhook_url = models.URLField(_('Webhook URL'), blank=True)
    
    # Банківські реквізити
    iban = models.CharField(_('IBAN'), max_length=29, blank=True)
    recipient_name = models.CharField(_("Ім'я отримувача"), max_length=200, blank=True)
    recipient_code = models.CharField(_('Код отримувача'), max_length=20, blank=True)
    
    is_active = models.BooleanField(_('Активні'), default=True)
    
    created_at = models.DateTimeField(_('Створено'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Оновлено'), auto_now=True)
    
    class Meta:
        verbose_name = _('Налаштування платежів')
        verbose_name_plural = _('Налаштування платежів')
    
    def __str__(self):
        return f"Платежі - {self.company_name}"


class AnalyticsEvent(models.Model):
    """Кастомні події аналітики"""
    
    EVENT_TYPES = [
        ('page_view', _('Перегляд сторінки')),
        ('form_submit', _('Відправка форми')),
        ('download', _('Завантаження')),
        ('contact', _('Контакт')),
        ('product_view', _('Перегляд продукту')),
    ]
    
    event_type = models.CharField(_('Тип події'), max_length=20, choices=EVENT_TYPES)
    event_name = models.CharField(_('Назва події'), max_length=100)
    page_url = models.URLField(_('URL сторінки'), max_length=500)
    user_agent = models.TextField(_('User Agent'), blank=True)
    ip_address = models.GenericIPAddressField(_('IP адреса'), blank=True, null=True)
    
    # Додаткові дані (JSON)
    extra_data = models.JSONField(_('Додаткові дані'), default=dict, blank=True)
    
    created_at = models.DateTimeField(_('Створено'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Подія аналітики')
        verbose_name_plural = _('Події аналітики')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_event_type_display()}: {self.event_name}"
