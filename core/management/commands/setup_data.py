from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from core.models import SiteSettings, Language, Menu, MenuItem
from pages.models import Page, Hero, Partner
# Продукти створюються окремою командою setup_products


class Command(BaseCommand):
    help = 'Налаштування базових даних для сайту'

    def handle(self, *args, **options):
        self.stdout.write('Створення базових даних...')
        
        # Створення мов
        self.create_languages()
        
        # Створення налаштувань сайту
        self.create_site_settings()
        
        # Створення меню
        self.create_menus()
        
        # Створення сторінок
        self.create_pages()
        
        # Створення hero секцій
        self.create_hero_sections()
        
        # Створення партнерів
        self.create_partners()
        
        self.stdout.write(
            self.style.SUCCESS('Базові дані успішно створено!')
        )
        self.stdout.write(
            self.style.WARNING('Для створення продуктів запустіть: python manage.py setup_products')
        )

    def create_languages(self):
        """Створення мов"""
        languages_data = [
            {'code': 'uk', 'name': 'Ukrainian', 'name_local': 'Українська', 'is_default': True},
            {'code': 'ru', 'name': 'Russian', 'name_local': 'Русский', 'is_default': False},
            {'code': 'en', 'name': 'English', 'name_local': 'English', 'is_default': False},
        ]
        
        for lang_data in languages_data:
            Language.objects.get_or_create(
                code=lang_data['code'],
                defaults=lang_data
            )
            self.stdout.write(f'Мова {lang_data["name_local"]} створена')

    def create_site_settings(self):
        """Створення налаштувань сайту"""
        settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Adiabatic',
                'site_description': 'Промислове обладнання та послуги',
                'contact_email': 'info@adiabatic.com',
                'contact_phone': '+380 44 123 45 67',
                'address': 'Київ, Україна',
                'meta_title': 'Adiabatic - Промислове обладнання',
                'meta_description': 'Промислове обладнання та послуги від компанії Adiabatic',
                'meta_keywords': 'промислове обладнання, adiabatic, промисловість',
            }
        )
        
        if created:
            self.stdout.write('Налаштування сайту створено')
        else:
            self.stdout.write('Налаштування сайту вже існують')

    def create_menus(self):
        """Створення меню"""
        # Верхнє меню
        header_menu, created = Menu.objects.get_or_create(
            menu_type='header',
            defaults={'name': 'Верхнє меню', 'is_active': True}
        )
        
        if created:
            self.stdout.write('Верхнє меню створено')
        
        # Створення елементів меню
        menu_items = [
            {'title': 'Головна', 'url': '/', 'order': 1},
            {'title': 'Про компанію', 'url': '/about/', 'order': 2},
            {'title': 'Продукція', 'url': '/products/', 'order': 3},
            {'title': 'Контакти', 'url': '/contacts/', 'order': 4},
        ]
        
        for item_data in menu_items:
            MenuItem.objects.get_or_create(
                menu=header_menu,
                title=item_data['title'],
                defaults={
                    'url': item_data['url'],
                    'order': item_data['order'],
                    'is_active': True
                }
            )
        
        self.stdout.write('Елементи меню створено')

    def create_pages(self):
        """Створення основних сторінок"""
        pages_data = [
            {
                'page_type': 'home',
                'slug': 'home',
                'title_uk': 'Головна сторінка',
                'title_ru': 'Главная страница',
                'title_en': 'Home page',
                'content_uk': 'Ласкаво просимо на сайт компанії Adiabatic. Ми спеціалізуємося на промисловому обладнанні та послугах.',
                'content_ru': 'Добро пожаловать на сайт компании Adiabatic. Мы специализируемся на промышленном оборудовании и услугах.',
                'content_en': 'Welcome to Adiabatic company website. We specialize in industrial equipment and services.',
            },
            {
                'page_type': 'about',
                'slug': 'about',
                'title_uk': 'Про компанію',
                'title_ru': 'О компании',
                'title_en': 'About company',
                'content_uk': 'Компанія Adiabatic - це надійний партнер у сфері промислового обладнання. Ми маємо багаторічний досвід та забезпечуємо якісні послуги.',
                'content_ru': 'Компания Adiabatic - это надежный партнер в сфере промышленного оборудования. Мы имеем многолетний опыт и обеспечиваем качественные услуги.',
                'content_en': 'Adiabatic company is a reliable partner in industrial equipment. We have years of experience and provide quality services.',
            },
            {
                'page_type': 'contacts',
                'slug': 'contacts',
                'title_uk': 'Контакти',
                'title_ru': 'Контакты',
                'title_en': 'Contacts',
                'content_uk': 'Зв\'яжіться з нами для отримання додаткової інформації про наші послуги та обладнання.',
                'content_ru': 'Свяжитесь с нами для получения дополнительной информации о наших услугах и оборудовании.',
                'content_en': 'Contact us for more information about our services and equipment.',
            },
            {
                'page_type': 'products',
                'slug': 'products',
                'title_uk': 'Продукція',
                'title_ru': 'Продукция',
                'title_en': 'Products',
                'content_uk': 'Наша продукція включає широкий спектр промислового обладнання для різних галузей.',
                'content_ru': 'Наша продукция включает широкий спектр промышленного оборудования для различных отраслей.',
                'content_en': 'Our products include a wide range of industrial equipment for various industries.',
            },
        ]
        
        for page_data in pages_data:
            Page.objects.get_or_create(
                page_type=page_data['page_type'],
                defaults=page_data
            )
        
        self.stdout.write('Основні сторінки створено')

    def create_hero_sections(self):
        """Створення hero секцій"""
        hero_data = {
            'title_uk': 'Промислове обладнання Adiabatic',
            'title_ru': 'Промышленное оборудование Adiabatic',
            'title_en': 'Adiabatic Industrial Equipment',
            'subtitle_uk': 'Якість та надійність',
            'subtitle_ru': 'Качество и надежность',
            'subtitle_en': 'Quality and reliability',
            'description_uk': 'Ми забезпечуємо промислові підприємства сучасним обладнанням та технологіями для підвищення ефективності виробництва.',
            'description_ru': 'Мы обеспечиваем промышленные предприятия современным оборудованием и технологиями для повышения эффективности производства.',
            'description_en': 'We provide industrial enterprises with modern equipment and technologies to improve production efficiency.',
            'cta_text_uk': 'Дізнатися більше',
            'cta_text_ru': 'Узнать больше',
            'cta_text_en': 'Learn more',
            'cta_url': '/about/',
            'is_active': True,
            'order': 1,
        }
        
        Hero.objects.get_or_create(
            title_uk=hero_data['title_uk'],
            defaults=hero_data
        )
        
        self.stdout.write('Hero секції створено')

    def create_partners(self):
        """Створення партнерів"""
        partners_data = [
            {
                'name': 'Промислові рішення',
                'description': 'Партнер з промислових рішень',
                'website_url': 'https://example.com',
            },
            {
                'name': 'Технології майбутнього',
                'description': 'Інноваційні технології',
                'website_url': 'https://example.com',
            },
            {
                'name': 'Промислові системи',
                'description': 'Системи автоматизації',
                'website_url': 'https://example.com',
            },
        ]
        
        for partner_data in partners_data:
            Partner.objects.get_or_create(
                name=partner_data['name'],
                defaults=partner_data
            )
        
        self.stdout.write('Партнери створено')
