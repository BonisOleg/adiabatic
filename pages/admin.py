from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Page, Section, Hero, Partner


class SectionInline(admin.TabularInline):
    """Inline для секцій сторінки"""
    model = Section
    extra = 1
    fields = ['section_type', 'title', 'content', 'order', 'is_published']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    """Адмінка для сторінок"""
    list_display = ['page_type', 'title_uk', 'is_published', 'created_at', 'updated_at']
    list_filter = ['page_type', 'is_published', 'created_at']
    search_fields = ['title_uk', 'title_ru', 'title_en']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [SectionInline]
    
    fieldsets = (
        (_('Основна інформація'), {
            'fields': ('page_type', 'slug', 'is_published')
        }),
        (_('Українська мова'), {
            'fields': ('title_uk', 'content_uk', 'meta_title_uk', 'meta_description_uk')
        }),
        (_('Російська мова'), {
            'fields': ('title_ru', 'content_ru', 'meta_title_ru', 'meta_description_ru')
        }),
        (_('Англійська мова'), {
            'fields': ('title_en', 'content_en', 'meta_title_en', 'meta_description_en')
        }),
    )


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    """Адмінка для секцій"""
    list_display = ['page', 'section_type', 'title', 'order', 'is_published']
    list_filter = ['section_type', 'is_published', 'page']
    search_fields = ['title', 'page__title_uk']
    ordering = ['page', 'order']
    list_editable = ['order', 'is_published']


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    """Адмінка для hero секцій"""
    list_display = ['title_uk', 'subtitle_uk', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['title_uk', 'title_ru', 'title_en']
    ordering = ['order']
    list_editable = ['is_active', 'order']
    
    fieldsets = (
        (_('Основна інформація'), {
            'fields': ('background_image', 'is_active', 'order')
        }),
        (_('Українська мова'), {
            'fields': ('title_uk', 'subtitle_uk', 'description_uk', 'cta_text_uk')
        }),
        (_('Російська мова'), {
            'fields': ('title_ru', 'subtitle_ru', 'description_ru', 'cta_text_ru')
        }),
        (_('Англійська мова'), {
            'fields': ('title_en', 'subtitle_en', 'description_en', 'cta_text_en')
        }),
        (_('Кнопка'), {
            'fields': ('cta_url',)
        }),
    )


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    """Адмінка для партнерів"""
    list_display = ['name', 'website_url', 'order', 'is_published']
    list_filter = ['is_published']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    list_editable = ['order', 'is_published']
