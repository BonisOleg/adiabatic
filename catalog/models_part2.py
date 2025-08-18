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
