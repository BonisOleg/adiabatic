from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SiteSettings, Language, Menu, MenuItem, PaymentSettings, AnalyticsEvent


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Адмінка для налаштувань сайту"""
    list_display = ['site_name', 'contact_email', 'contact_phone', 'updated_at']
    fieldsets = (
        (_('Основна інформація'), {
            'fields': ('site_name', 'site_description', 'contact_email', 'contact_phone', 'address')
        }),
        (_('SEO налаштування'), {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        (_('Соціальні мережі'), {
            'fields': ('facebook_url', 'instagram_url', 'linkedin_url')
        }),
        (_('Аналітика'), {
            'fields': ('google_analytics_id', 'yandex_metrika_id')
        }),
    )
    
    def has_add_permission(self, request):
        """Дозволити створення тільки одного об'єкта"""
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Заборонити видалення"""
        return False


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """Адмінка для мов"""
    list_display = ['code', 'name', 'name_local', 'is_active', 'is_default']
    list_editable = ['is_active', 'is_default']
    search_fields = ['code', 'name', 'name_local']
    ordering = ['-is_default', 'name']


class MenuItemInline(admin.TabularInline):
    """Inline для елементів меню"""
    model = MenuItem
    extra = 1
    fields = ['title', 'url', 'page', 'order', 'is_active', 'is_external', 'open_in_new_tab']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """Адмінка для меню"""
    list_display = ['name', 'menu_type', 'is_active', 'items_count']
    list_filter = ['menu_type', 'is_active']
    search_fields = ['name']
    inlines = [MenuItemInline]
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = _('Кількість елементів')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Адмінка для елементів меню"""
    list_display = ['title', 'menu', 'parent', 'order', 'is_active']
    list_filter = ['menu', 'is_active', 'is_external']
    search_fields = ['title', 'url']
    ordering = ['menu', 'order']
    list_editable = ['order', 'is_active']


@admin.register(PaymentSettings)
class PaymentSettingsAdmin(admin.ModelAdmin):
    """Адмінка для налаштувань платежів"""
    list_display = ['company_name', 'is_active', 'created_at', 'updated_at']
    fieldsets = (
        (_('Основна інформація'), {
            'fields': ('company_name', 'description', 'is_active')
        }),
        (_('Monobank інтеграція'), {
            'fields': ('monobank_token', 'monobank_webhook_url')
        }),
        (_('Банківські реквізити'), {
            'fields': ('iban', 'recipient_name', 'recipient_code')
        }),
    )
    
    def has_add_permission(self, request):
        """Дозволити створення тільки одного об'єкта"""
        return not PaymentSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Заборонити видалення"""
        return False


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    """Адмінка для подій аналітики"""
    list_display = ['event_name', 'event_type', 'page_url', 'ip_address', 'created_at']
    list_filter = ['event_type', 'created_at']
    search_fields = ['event_name', 'page_url', 'ip_address']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Подія'), {
            'fields': ('event_type', 'event_name', 'page_url')
        }),
        (_('Користувач'), {
            'fields': ('ip_address', 'user_agent')
        }),
        (_('Додаткові дані'), {
            'fields': ('extra_data',)
        }),
        (_('Мета-дані'), {
            'fields': ('created_at',)
        }),
    )
    
    def has_add_permission(self, request):
        """Заборонити ручне створення"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Дозволити тільки перегляд"""
        return True
    
    def has_delete_permission(self, request, obj=None):
        """Дозволити видалення старих записів"""
        return True
