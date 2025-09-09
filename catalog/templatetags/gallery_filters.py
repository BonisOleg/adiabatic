from django import template

register = template.Library()

@register.filter
def has_3d_model(gallery_items):
    """Перевіряє чи є в галереї 3D модель"""
    for item in gallery_items:
        if item.content_type == '3D_MODEL':
            return True
    return False

@register.filter
def first_3d_model(gallery_items):
    """Повертає першу 3D модель з галереї"""
    for item in gallery_items:
        if item.content_type == '3D_MODEL':
            return item
    return None

@register.filter
def first_image(gallery_items):
    """Повертає перше зображення з галереї"""
    for item in gallery_items:
        if item.content_type == 'IMAGE':
            return item
    return None
