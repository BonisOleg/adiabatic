from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Product, ProductSpec, ProductGallery, ProductAdvantage, ProductDocument


class ProductSpecInline(admin.TabularInline):
    """Inline для технічних характеристик"""
    model = ProductSpec
    extra = 3
    fields = ['name_uk', 'name_ru', 'name_en', 'value', 'unit', 'order']


class ProductGalleryInline(admin.TabularInline):
    """Inline для мультимедійної галереї"""
    model = ProductGallery
    extra = 2
    fields = ['content_type', 'image', 'file_3d', 'preview_image', 'title_uk', 'alt_text', 'order', 'is_downloadable']
    readonly_fields = ['file_size', 'download_count']


class ProductAdvantageInline(admin.TabularInline):
    """Inline для переваг продукту"""
    model = ProductAdvantage
    extra = 2
    fields = ['title_uk', 'title_ru', 'title_en', 'description_uk', 'icon', 'order']


class ProductDocumentInline(admin.TabularInline):
    """Inline для документів продукту"""
    model = ProductDocument
    extra = 1
    fields = ['document_type', 'title_uk', 'file', 'qr_code', 'is_public', 'order']
    readonly_fields = ['access_count', 'qr_uuid']





@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Адмінка для категорій"""
    list_display = ['name_uk', 'name_ru', 'name_en', 'order', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['name_uk', 'name_ru', 'name_en']
    list_editable = ['order', 'is_published']
    prepopulated_fields = {'slug': ('name_en',)}
    
    fieldsets = (
        (_('Основна інформація'), {
            'fields': ('slug', 'icon', 'order', 'is_published')
        }),
        (_('Українська мова'), {
            'fields': ('name_uk', 'description_uk')
        }),
        (_('Російська мова'), {
            'fields': ('name_ru', 'description_ru')
        }),
        (_('Англійська мова'), {
            'fields': ('name_en', 'description_en')
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Адмінка для продуктів"""
    list_display = ['name_uk', 'category', 'application_type', 'power_kw', 'price_usd', 'is_featured', 'is_published']
    list_filter = ['category', 'application_type', 'fluid_type', 'is_featured', 'is_published', 'created_at']
    search_fields = ['name_uk', 'name_ru', 'name_en', 'short_description_uk', 'standards']
    list_editable = ['is_featured', 'is_published', 'price_usd']
    prepopulated_fields = {'slug': ('name_en',)}
    readonly_fields = ['created_at', 'updated_at']
    
    inlines = [ProductSpecInline, ProductGalleryInline, ProductAdvantageInline, ProductDocumentInline]
    
    fieldsets = (
        (_('Основна інформація'), {
            'fields': ('category', 'slug', 'hero_image', 'price_usd', 'is_featured', 'is_published')
        }),
        (_('Технічні характеристики'), {
            'fields': ('application_type', 'fluid_type', 'power_kw', 'max_pressure_bar', 'max_temperature_c', 'standards'),
            'classes': ('wide',)
        }),
        (_('Матеріали'), {
            'fields': ('material_shell', 'material_tubes'),
            'classes': ('collapse',)
        }),
        (_('Українська мова'), {
            'fields': ('name_uk', 'short_description_uk', 'description_uk', 'meta_title_uk', 'meta_description_uk')
        }),
        (_('Російська мова'), {
            'fields': ('name_ru', 'short_description_ru', 'description_ru', 'meta_title_ru', 'meta_description_ru')
        }),
        (_('Англійська мова'), {
            'fields': ('name_en', 'short_description_en', 'description_en', 'meta_title_en', 'meta_description_en')
        }),
        (_('Дати'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


@admin.register(ProductSpec)
class ProductSpecAdmin(admin.ModelAdmin):
    """Адмінка для технічних характеристик"""
    list_display = ['product', 'name_uk', 'value', 'unit', 'order']
    list_filter = ['product__category']
    search_fields = ['product__name_uk', 'name_uk', 'value']
    list_editable = ['order']
    
    fieldsets = (
        (_('Основна інформація'), {
            'fields': ('product', 'value', 'unit', 'order')
        }),
        (_('Мультимовні назви'), {
            'fields': ('name_uk', 'name_ru', 'name_en')
        }),
    )


@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    """Адмінка для мультимедійної галереї"""
    list_display = ['product', 'content_type', 'get_title', 'get_preview_thumb', 'download_count', 'order', 'is_downloadable']
    list_filter = ['content_type', 'product__category', 'is_downloadable']
    search_fields = ['product__name_uk', 'title_uk', 'alt_text', 'description']
    list_editable = ['order', 'is_downloadable']
    readonly_fields = ['file_size', 'download_count', 'created_at']
    
    fieldsets = (
        (_('Основна інформація'), {
            'fields': ('product', 'content_type', 'order', 'is_downloadable')
        }),
        (_('Файли'), {
            'fields': ('image', 'file_3d', 'preview_image')
        }),
        (_('Мультимовні назви'), {
            'fields': ('title_uk', 'title_ru', 'title_en', 'alt_text', 'description')
        }),
        (_('Статистика'), {
            'fields': ('file_size', 'download_count', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_preview_thumb(self, obj):
        """Показати мініатюру превью"""
        preview = obj.get_preview()
        if preview:
            return f'<img src="{preview.url}" width="50" height="50" style="object-fit: cover;" />'
        return '-'
    get_preview_thumb.short_description = _('Превью')
    get_preview_thumb.allow_tags = True


@admin.register(ProductAdvantage)
class ProductAdvantageAdmin(admin.ModelAdmin):
    """Адмінка для переваг"""
    list_display = ['product', 'title_uk', 'icon', 'order']
    list_filter = ['product__category']
    search_fields = ['product__name_uk', 'title_uk']
    list_editable = ['order']
    
    fieldsets = (
        (_('Основна інформація'), {
            'fields': ('product', 'icon', 'order')
        }),
        (_('Українська мова'), {
            'fields': ('title_uk', 'description_uk')
        }),
        (_('Російська мова'), {
            'fields': ('title_ru', 'description_ru')
        }),
        (_('Англійська мова'), {
            'fields': ('title_en', 'description_en')
        }),
    )


@admin.register(ProductDocument)
class ProductDocumentAdmin(admin.ModelAdmin):
    """Адмінка для документів продукту"""
    list_display = ['product', 'get_title', 'document_type', 'is_public', 'access_count', 'order']
    list_filter = ['document_type', 'is_public', 'product__category', 'created_at']
    search_fields = ['product__name_uk', 'title_uk', 'title_ru', 'title_en']
    list_editable = ['is_public', 'order']
    readonly_fields = ['qr_uuid', 'access_count', 'created_at', 'updated_at']
    
    fieldsets = (
        (_('Основна інформація'), {
            'fields': ('product', 'document_type', 'file', 'order', 'is_public')
        }),
        (_('QR код'), {
            'fields': ('qr_code', 'qr_uuid'),
            'classes': ('collapse',)
        }),
        (_('Мультимовні назви'), {
            'fields': ('title_uk', 'title_ru', 'title_en')
        }),
        (_('Статистика'), {
            'fields': ('access_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_title(self, obj):
        """Отримати назву документу"""
        return obj.get_title()
    get_title.short_description = _('Назва')


