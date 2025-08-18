from .models import SiteSettings, Language, Menu


def site_settings(request):
    """Додає глобальні налаштування сайту до контексту"""
    try:
        site_settings_obj = SiteSettings.get_settings()
    except Exception:
        site_settings_obj = None
    
    try:
        languages = Language.objects.filter(is_active=True)
    except Exception:
        languages = []
    
    try:
        header_menu = Menu.objects.filter(menu_type='header', is_active=True).first()
    except Exception:
        header_menu = None
    
    try:
        footer_menu = Menu.objects.filter(menu_type='footer', is_active=True).first()
    except Exception:
        footer_menu = None
    
    try:
        mobile_menu = Menu.objects.filter(menu_type='mobile', is_active=True).first()
    except Exception:
        mobile_menu = None
    
    return {
        'site_settings': site_settings_obj,
        'languages': languages,
        'header_menu': header_menu,
        'footer_menu': footer_menu,
        'mobile_menu': mobile_menu,
    }
