from .models import SiteSettings, Language, Menu


def site_settings(request):
    """Додає глобальні налаштування сайту до контексту"""
    return {
        'site_settings': SiteSettings.get_settings(),
        'languages': Language.objects.filter(is_active=True),
        'header_menu': Menu.objects.filter(menu_type='header', is_active=True).first(),
        'footer_menu': Menu.objects.filter(menu_type='footer', is_active=True).first(),
        'mobile_menu': Menu.objects.filter(menu_type='mobile', is_active=True).first(),
    }
