from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Категорії продуктів"""
    
    name_uk = models.CharField(_('Назва (УК)'), max_length=100)
    name_ru = models.CharField(_('Назва (РУ)'), max_length=100)
    name_en = models.CharField(_('Назва (EN)'), max_length=100)
    
    slug = models.SlugField(_('Slug'), max_length=120, unique=True, blank=True)
    
    description_uk = models.TextField(_('Опис (УК)'), blank=True)
    description_ru = models.TextField(_('Опис (РУ)'), blank=True)
    description_en = models.TextField(_('Опис (EN)'), blank=True)
    
    icon = models.CharField(_('Іконка'), max_length=50, blank=True, 
                           help_text=_('CSS клас іконки (наприклад: fas fa-cog)'))
    
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    is_published = models.BooleanField(_('Опубліковано'), default=True)
    
    created_at = models.DateTimeField(_('Створено'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Оновлено'), auto_now=True)
    
    class Meta:
        verbose_name = _('Категорія')
        verbose_name_plural = _('Категорії')
        ordering = ['order', 'name_uk']
    
    def __str__(self):
        return self.name_uk
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en or self.name_uk)
        super().save(*args, **kwargs)
    
    def get_name(self):
        """Отримати назву залежно від поточної мови"""
        from django.utils.translation import get_language
        lang = get_language()
        if lang == 'ru':
            return self.name_ru
        elif lang == 'en':
            return self.name_en
        return self.name_uk
    
    def get_description(self):
        """Отримати опис залежно від поточної мови"""
        from django.utils.translation import get_language
        lang = get_language()
        if lang == 'ru':
            return self.description_ru
        elif lang == 'en':
            return self.description_en
        return self.description_uk


class Product(models.Model):
    """Продукти компанії"""
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                verbose_name=_('Категорія'), related_name='products')
    
    name_uk = models.CharField(_('Назва (УК)'), max_length=200)
    name_ru = models.CharField(_('Назва (РУ)'), max_length=200)
    name_en = models.CharField(_('Назва (EN)'), max_length=200)
    
    slug = models.SlugField(_('Slug'), max_length=220, unique=True, blank=True)
    
    short_description_uk = models.TextField(_('Короткий опис (УК)'), max_length=300)
    short_description_ru = models.TextField(_('Короткий опис (РУ)'), max_length=300)
    short_description_en = models.TextField(_('Короткий опис (EN)'), max_length=300)
    
    description_uk = models.TextField(_('Повний опис (УК)'))
    description_ru = models.TextField(_('Повний опис (РУ)'))
    description_en = models.TextField(_('Повний опис (EN)'))
    
    hero_image = models.ImageField(_('Головне зображення'), upload_to='products/hero/', 
                                  blank=True, null=True)
    
    price_usd = models.DecimalField(_('Ціна (USD)'), max_digits=10, decimal_places=2, 
                                   blank=True, null=True)
    
    meta_title_uk = models.CharField(_('Meta заголовок (УК)'), max_length=60, blank=True)
    meta_title_ru = models.CharField(_('Meta заголовок (РУ)'), max_length=60, blank=True)
    meta_title_en = models.CharField(_('Meta заголовок (EN)'), max_length=60, blank=True)
    
    meta_description_uk = models.CharField(_('Meta опис (УК)'), max_length=160, blank=True)
    meta_description_ru = models.CharField(_('Meta опис (РУ)'), max_length=160, blank=True)
    meta_description_en = models.CharField(_('Meta опис (EN)'), max_length=160, blank=True)
    
    is_featured = models.BooleanField(_('Рекомендований'), default=False)
    is_published = models.BooleanField(_('Опубліковано'), default=True)
    
    created_at = models.DateTimeField(_('Створено'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Оновлено'), auto_now=True)
    
    class Meta:
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукти')
        ordering = ['-is_featured', 'category__order', 'name_uk']
    
    def __str__(self):
        return self.name_uk
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en or self.name_uk)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})
    
    def get_name(self):
        from django.utils.translation import get_language
        lang = get_language()
        if lang == 'ru':
            return self.name_ru
        elif lang == 'en':
            return self.name_en
        return self.name_uk
    
    def get_short_description(self):
        from django.utils.translation import get_language
        lang = get_language()
        if lang == 'ru':
            return self.short_description_ru
        elif lang == 'en':
            return self.short_description_en
        return self.short_description_uk
    
    def get_description(self):
        from django.utils.translation import get_language
        lang = get_language()
        if lang == 'ru':
            return self.description_ru
        elif lang == 'en':
            return self.description_en
        return self.description_uk
    
    def get_meta_title(self):
        from django.utils.translation import get_language
        lang = get_language()
        if lang == 'ru' and self.meta_title_ru:
            return self.meta_title_ru
        elif lang == 'en' and self.meta_title_en:
            return self.meta_title_en
        elif self.meta_title_uk:
            return self.meta_title_uk
        return self.get_name()
    
    def get_meta_description(self):
        from django.utils.translation import get_language
        lang = get_language()
        if lang == 'ru' and self.meta_description_ru:
            return self.meta_description_ru
        elif lang == 'en' and self.meta_description_en:
            return self.meta_description_en
        elif self.meta_description_uk:
            return self.meta_description_uk
        return self.get_short_description()
class ProductSpec(models.Model):
    """Технічні характеристики продукту"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                               verbose_name=_('Продукт'), related_name='specifications')
    
    name_uk = models.CharField(_('Характеристика (УК)'), max_length=100)
    name_ru = models.CharField(_('Характеристика (РУ)'), max_length=100)
    name_en = models.CharField(_('Характеристика (EN)'), max_length=100)
    
    value = models.CharField(_('Значення'), max_length=200)
    unit = models.CharField(_('Одиниця виміру'), max_length=20, blank=True)
    
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    
    class Meta:
        verbose_name = _('Технічна характеристика')
        verbose_name_plural = _('Технічні характеристики')
        ordering = ['order', 'name_uk']
    
    def __str__(self):
        unit_str = f" {self.unit}" if self.unit else ""
        return f"{self.name_uk}: {self.value}{unit_str}"
    
    def get_name(self):
        from django.utils.translation import get_language
        lang = get_language()
        if lang == 'ru':
            return self.name_ru
        elif lang == 'en':
            return self.name_en
        return self.name_uk


class ProductGallery(models.Model):
    """Галерея зображень продукту"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                               verbose_name=_('Продукт'), related_name='gallery')
    
    image = models.ImageField(_('Зображення'), upload_to='products/gallery/')
    alt_text = models.CharField(_('Alt текст'), max_length=200, blank=True)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    
    class Meta:
        verbose_name = _('Зображення галереї')
        verbose_name_plural = _('Галерея продукту')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.product.name_uk} - Зображення {self.order}"


class ProductAdvantage(models.Model):
    """Переваги продукту"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                               verbose_name=_('Продукт'), related_name='advantages')
    
    title_uk = models.CharField(_('Заголовок (УК)'), max_length=100)
    title_ru = models.CharField(_('Заголовок (РУ)'), max_length=100)
    title_en = models.CharField(_('Заголовок (EN)'), max_length=100)
    
    description_uk = models.TextField(_('Опис (УК)'), max_length=300)
    description_ru = models.TextField(_('Опис (РУ)'), max_length=300)
    description_en = models.TextField(_('Опис (EN)'), max_length=300)
    
    icon = models.CharField(_('Іконка'), max_length=50, blank=True,
                           help_text=_('CSS клас іконки (наприклад: fas fa-check)'))
    
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    
    class Meta:
        verbose_name = _('Перевага продукту')
        verbose_name_plural = _('Переваги продукту')
        ordering = ['order']
    
    def __str__(self):
        return self.title_uk
    
    def get_title(self):
        from django.utils.translation import get_language
        lang = get_language()
        if lang == 'ru':
            return self.title_ru
        elif lang == 'en':
            return self.title_en
        return self.title_uk
    
    def get_description(self):
        from django.utils.translation import get_language
        lang = get_language()
        if lang == 'ru':
            return self.description_ru
        elif lang == 'en':
            return self.description_en
        return self.description_uk


class ProductDocument(models.Model):
    """Документи та сертифікати продукту"""
    
    DOCUMENT_TYPES = (
        ('certificate', _('Сертифікат')),
        ('manual', _('Інструкція')),
        ('datasheet', _('Технічний лист')),
        ('warranty', _('Гарантія')),
        ('other', _('Інше')),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                               verbose_name=_('Продукт'), related_name='documents')
    
    title_uk = models.CharField(_('Назва документу (УК)'), max_length=200)
    title_ru = models.CharField(_('Назва документу (РУ)'), max_length=200)
    title_en = models.CharField(_('Назва документу (EN)'), max_length=200)
    
    document_type = models.CharField(_('Тип документу'), max_length=20, 
                                    choices=DOCUMENT_TYPES, default='other')
    
    file = models.FileField(_('Файл'), upload_to='products/documents/')
    
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    is_public = models.BooleanField(_('Публічний'), default=True)
    
    created_at = models.DateTimeField(_('Створено'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Документ продукту')
        verbose_name_plural = _('Документи продукту')
        ordering = ['order', 'document_type']
    
    def __str__(self):
        return self.title_uk
    
    def get_title(self):
        from django.utils.translation import get_language
        lang = get_language()
        if lang == 'ru':
            return self.title_ru
        elif lang == 'en':
            return self.title_en
        return self.title_uk
