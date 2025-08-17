from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SiteSettings, Language, Menu, MenuItem


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
