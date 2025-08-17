from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify


class Page(models.Model):
    """Основні сторінки сайту"""
    PAGE_TYPES = [
        ('home', _('Головна')),
        ('about', _('Про компанію')),
        ('contacts', _('Контакти')),
        ('products', _('Продукція')),
        ('custom', _('Кастомна сторінка')),
    ]
    
    page_type = models.CharField(_('Тип сторінки'), max_length=20, choices=PAGE_TYPES, unique=True)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True, blank=True)
    
    # Мультимовні поля
    title_uk = models.CharField(_('Заголовок (укр)'), max_length=200)
    title_ru = models.CharField(_('Заголовок (рус)'), max_length=200)
    title_en = models.CharField(_('Заголовок (англ)'), max_length=200)
    
    content_uk = models.TextField(_('Контент (укр)'), blank=True)
    content_ru = models.TextField(_('Контент (рус)'), blank=True)
    content_en = models.TextField(_('Контент (англ)'), blank=True)
    
    # SEO поля
    meta_title_uk = models.CharField(_('Meta title (укр)'), max_length=60, blank=True)
    meta_title_ru = models.CharField(_('Meta title (рус)'), max_length=60, blank=True)
    meta_title_en = models.CharField(_('Meta title (англ)'), max_length=60, blank=True)
    
    meta_description_uk = models.TextField(_('Meta description (укр)'), max_length=160, blank=True)
    meta_description_ru = models.TextField(_('Meta description (рус)'), max_length=160, blank=True)
    meta_description_en = models.TextField(_('Meta description (англ)'), max_length=160, blank=True)
    
    is_published = models.BooleanField(_('Опубліковано'), default=True)
    created_at = models.DateTimeField(_('Створено'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Оновлено'), auto_now=True)
    
    class Meta:
        verbose_name = _('Сторінка')
        verbose_name_plural = _('Сторінки')
        ordering = ['page_type']
    
    def __str__(self):
        return f"{self.get_page_type_display()}: {self.title_uk}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_uk)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Отримати абсолютний URL для сторінки"""
        if self.page_type == 'home':
            return reverse('pages:home')
        elif self.page_type == 'about':
            return reverse('pages:about')
        elif self.page_type == 'contacts':
            return reverse('pages:contacts')
        elif self.page_type == 'products':
            return reverse('pages:products')
        else:
            return reverse('pages:page_detail', kwargs={'slug': self.slug})
    
    def get_title(self, language_code='uk'):
        """Отримати заголовок для конкретної мови"""
        return getattr(self, f'title_{language_code}', self.title_uk)
    
    def get_content(self, language_code='uk'):
        """Отримати контент для конкретної мови"""
        return getattr(self, f'content_{language_code}', self.content_uk)
    
    def get_meta_title(self, language_code='uk'):
        """Отримати meta title для конкретної мови"""
        return getattr(self, f'meta_title_{language_code}', self.title_uk)
    
    def get_meta_description(self, language_code='uk'):
        """Отримати meta description для конкретної мови"""
        return getattr(self, f'meta_description_{language_code}', self.content_uk[:160])


class Section(models.Model):
    """Секції сторінок (JSON конструктор)"""
    SECTION_TYPES = [
        ('hero', _('Hero секція')),
        ('text', _('Текстова секція')),
        ('image', _('Зображення')),
        ('gallery', _('Галерея')),
        ('features', _('Особливості')),
        ('testimonials', _('Відгуки')),
        ('cta', _('Call to Action')),
        ('contact', _('Контактна форма')),
    ]
    
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='sections', verbose_name=_('Сторінка'))
    section_type = models.CharField(_('Тип секції'), max_length=20, choices=SECTION_TYPES)
    title = models.CharField(_('Заголовок секції'), max_length=200, blank=True)
    content = models.JSONField(_('Контент секції'), default=dict)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    is_published = models.BooleanField(_('Опубліковано'), default=True)
    
    class Meta:
        verbose_name = _('Секція')
        verbose_name_plural = _('Секції')
        ordering = ['page', 'order']
    
    def __str__(self):
        return f"{self.page.get_page_type_display()}: {self.get_section_type_display()} - {self.title}"


class Hero(models.Model):
    """Hero секції для головної сторінки"""
    title_uk = models.CharField(_('Заголовок (укр)'), max_length=200)
    title_ru = models.CharField(_('Заголовок (рус)'), max_length=200)
    title_en = models.CharField(_('Заголовок (англ)'), max_length=200)
    
    subtitle_uk = models.CharField(_('Підзаголовок (укр)'), max_length=300, blank=True)
    subtitle_ru = models.CharField(_('Підзаголовок (рус)'), max_length=300, blank=True)
    subtitle_en = models.CharField(_('Підзаголовок (англ)'), max_length=300, blank=True)
    
    description_uk = models.TextField(_('Опис (укр)'), blank=True)
    description_ru = models.TextField(_('Опис (рус)'), blank=True)
    description_en = models.TextField(_('Опис (англ)'), blank=True)
    
    background_image = models.ImageField(_('Фонове зображення'), upload_to='hero/')
    cta_text_uk = models.CharField(_('Текст кнопки (укр)'), max_length=50, default=_('Дізнатися більше'))
    cta_text_ru = models.CharField(_('Текст кнопки (рус)'), max_length=50, default=_('Дізнатися більше'))
    cta_text_en = models.CharField(_('Текст кнопки (англ)'), max_length=50, default=_('Дізнатися більше'))
    cta_url = models.CharField(_('URL кнопки'), max_length=200, blank=True)
    
    is_active = models.BooleanField(_('Активна'), default=True)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    
    class Meta:
        verbose_name = _('Hero секція')
        verbose_name_plural = _('Hero секції')
        ordering = ['order']
    
    def __str__(self):
        return f"Hero: {self.title_uk}"
    
    def get_title(self, language_code='uk'):
        return getattr(self, f'title_{language_code}', self.title_uk)
    
    def get_subtitle(self, language_code='uk'):
        return getattr(self, f'subtitle_{language_code}', self.subtitle_uk)
    
    def get_description(self, language_code='uk'):
        return getattr(self, f'description_{language_code}', self.description_uk)
    
    def get_cta_text(self, language_code='uk'):
        return getattr(self, f'cta_text_{language_code}', self.cta_text_uk)


class Partner(models.Model):
    """Партнери компанії"""
    name = models.CharField(_('Назва'), max_length=200)
    logo = models.ImageField(_('Логотип'), upload_to='partners/')
    website_url = models.URLField(_('Веб-сайт'), blank=True)
    description = models.TextField(_('Опис'), blank=True)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    is_published = models.BooleanField(_('Опубліковано'), default=True)
    
    class Meta:
        verbose_name = _('Партнер')
        verbose_name_plural = _('Партнери')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
