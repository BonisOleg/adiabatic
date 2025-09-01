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
    
    # Типи застосування
    APPLICATION_TYPES = [
        ('INDUSTRIAL', _('Промислові системи')),
        ('ENERGY', _('Енергетичне обладнання')),
        ('COMPACT', _('Компактні рішення')),
        ('CUSTOM', _('Спеціальні рішення')),
        ('FOOD', _('Харчова промисловість')),
        ('OIL_GAS', _('Нафтогазова галузь')),
        ('HVAC', _('Системи кондиціонування')),
        ('MARINE', _('Морське обладнання')),
    ]
    
    # Типи теплоносіїв
    FLUID_TYPES = [
        ('WATER', _('Вода')),
        ('STEAM', _('Пара')),
        ('OIL', _('Мастило/Нафтопродукти')),
        ('GAS', _('Газ')),
        ('AIR', _('Повітря')),
        ('REFRIGERANT', _('Хладагент')),
        ('CHEMICAL', _('Хімічні речовини')),
        ('MIXED', _('Змішані середовища')),
    ]
    
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
    
    # Технічні характеристики
    application_type = models.CharField(_('Тип застосування'), max_length=20, 
                                       choices=APPLICATION_TYPES, blank=True)
    fluid_type = models.CharField(_('Тип теплоносія'), max_length=20, 
                                 choices=FLUID_TYPES, blank=True)
    
    power_kw = models.DecimalField(_('Потужність (kW)'), max_digits=10, decimal_places=2, 
                                  blank=True, null=True)
    max_pressure_bar = models.DecimalField(_('Макс. тиск (bar)'), max_digits=8, decimal_places=2, 
                                          blank=True, null=True)
    max_temperature_c = models.DecimalField(_('Макс. температура (°C)'), max_digits=6, decimal_places=1, 
                                           blank=True, null=True)
    
    # Стандарти та сертифікати
    standards = models.CharField(_('Стандарти'), max_length=200, blank=True,
                                help_text=_('ASME, DIN, GOST тощо'))
    
    # Матеріали
    material_shell = models.CharField(_('Матеріал корпусу'), max_length=100, blank=True)
    material_tubes = models.CharField(_('Матеріал трубок'), max_length=100, blank=True)
    
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
    """Мультимедійна галерея продукту"""
    
    CONTENT_TYPES = [
        ('IMAGE', _('Зображення')),
        ('3D_MODEL', _('3D модель')),
        ('TECHNICAL_DRAWING', _('Технічне креслення')),
        ('ANIMATION', _('Анімація')),
        ('VIDEO', _('Відео')),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                               verbose_name=_('Продукт'), related_name='gallery')
    
    content_type = models.CharField(_('Тип контенту'), max_length=20, 
                                   choices=CONTENT_TYPES, default='IMAGE')
    
    # Для зображень та відео
    image = models.ImageField(_('Зображення'), upload_to='products/gallery/', 
                             blank=True, null=True)
    
    # Для 3D моделей та креслень
    file_3d = models.FileField(_('3D модель/файл'), upload_to='products/3d/', 
                              blank=True, null=True,
                              help_text=_('Формати: .stp, .step, .iges, .obj, .gltf, .glb'))
    
    # Превью для 3D моделей
    preview_image = models.ImageField(_('Превью'), upload_to='products/3d/previews/', 
                                     blank=True, null=True,
                                     help_text=_('Зображення для превью 3D моделі'))
    
    title_uk = models.CharField(_('Назва (УК)'), max_length=200, blank=True)
    title_ru = models.CharField(_('Назва (РУ)'), max_length=200, blank=True)
    title_en = models.CharField(_('Назва (EN)'), max_length=200, blank=True)
    
    alt_text = models.CharField(_('Alt текст'), max_length=200, blank=True)
    description = models.TextField(_('Опис'), blank=True)
    
    # Технічні параметри для 3D
    file_size = models.CharField(_('Розмір файлу'), max_length=20, blank=True)
    download_count = models.PositiveIntegerField(_('Кількість завантажень'), default=0)
    
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    is_downloadable = models.BooleanField(_('Доступний для завантаження'), default=True)
    
    created_at = models.DateTimeField(_('Створено'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Елемент галереї')
        verbose_name_plural = _('Галерея продукту')
        ordering = ['order', 'content_type']
    
    def __str__(self):
        content_name = self.get_title() or f"{self.get_content_type_display()}"
        return f"{self.product.name_uk} - {content_name}"
    
    def get_title(self):
        """Отримати назву залежно від мови"""
        from django.utils.translation import get_language
        lang = get_language()
        if lang == 'ru' and self.title_ru:
            return self.title_ru
        elif lang == 'en' and self.title_en:
            return self.title_en
        return self.title_uk or self.alt_text
    
    def get_main_file(self):
        """Отримати основний файл для відображення"""
        if self.content_type == 'IMAGE':
            return self.image
        elif self.content_type in ['3D_MODEL', 'TECHNICAL_DRAWING']:
            return self.file_3d
        return None
    
    def get_preview(self):
        """Отримати превью файл"""
        if self.preview_image:
            return self.preview_image
        elif self.content_type == 'IMAGE' and self.image:
            return self.image
        return None
    
    def is_3d_viewable(self):
        """Чи можна переглянути 3D модель в браузері"""
        if not self.file_3d:
            return False
        ext = self.file_3d.name.lower().split('.')[-1]
        return ext in ['gltf', 'glb', 'obj']
    
    def increment_download(self):
        """Збільшити лічильник завантажень"""
        self.download_count += 1
        self.save(update_fields=['download_count'])


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


