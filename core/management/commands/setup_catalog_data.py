from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from catalog.models import Category, Product, ProductSpec, ProductAdvantage


class Command(BaseCommand):
    help = 'Створення тестових даних для каталогу продукції'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Початок створення тестових даних каталогу...'))
        
        # Створюємо категорії
        self.create_categories()
        
        # Створюємо продукти
        self.create_products()
        
        self.stdout.write(self.style.SUCCESS('✅ Тестові дані каталогу створені успішно!'))
    
    def create_categories(self):
        """Створення категорій продуктів"""
        categories_data = [
            {
                'name_uk': 'Теплообмінники',
                'name_ru': 'Теплообменники', 
                'name_en': 'Heat Exchangers',
                'slug': 'heat-exchangers',
                'description_uk': 'Високоефективні теплообмінники для промислових потреб',
                'description_ru': 'Высокоэффективные теплообменники для промышленных нужд',
                'description_en': 'High-efficiency heat exchangers for industrial needs',
                'icon': 'fas fa-thermometer-half',
                'order': 1,
            },
            {
                'name_uk': 'Кондиціонери',
                'name_ru': 'Кондиционеры',
                'name_en': 'Air Conditioners', 
                'slug': 'air-conditioners',
                'description_uk': 'Промислові системи кондиціонування повітря',
                'description_ru': 'Промышленные системы кондиционирования воздуха',
                'description_en': 'Industrial air conditioning systems',
                'icon': 'fas fa-wind',
                'order': 2,
            },
            {
                'name_uk': 'Вентиляційне обладнання',
                'name_ru': 'Вентиляционное оборудование',
                'name_en': 'Ventilation Equipment',
                'slug': 'ventilation-equipment', 
                'description_uk': 'Системи вентиляції та очищення повітря',
                'description_ru': 'Системы вентиляции и очистки воздуха',
                'description_en': 'Ventilation and air purification systems',
                'icon': 'fas fa-fan',
                'order': 3,
            },
        ]
        
        for data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            if created:
                self.stdout.write(f'✅ Створено категорію: {category.name_uk}')
            else:
                self.stdout.write(f'⚠️  Категорія вже існує: {category.name_uk}')
    
    def create_products(self):
        """Створення 10 продуктів"""
        products_data = [
            # Теплообмінники (4 продукти)
            {
                'category_slug': 'heat-exchangers',
                'name_uk': 'Пластинчастий теплообмінник АТ-100',
                'name_ru': 'Пластинчатый теплообменник АТ-100',
                'name_en': 'Plate Heat Exchanger AT-100',
                'slug': 'plate-heat-exchanger-at-100',
                'short_description_uk': 'Компактний пластинчастий теплообмінник з високою ефективністю',
                'short_description_ru': 'Компактный пластинчатый теплообменник с высокой эффективностью',
                'short_description_en': 'Compact plate heat exchanger with high efficiency',
                'description_uk': 'АТ-100 - це високоефективний пластинчастий теплообмінник, розроблений для промислових застосувань. Забезпечує відмінний теплообмін при мінімальних габаритах.',
                'description_ru': 'АТ-100 - это высокоэффективный пластинчатый теплообменник, разработанный для промышленных применений. Обеспечивает отличный теплообмен при минимальных габаритах.',
                'description_en': 'AT-100 is a high-efficiency plate heat exchanger designed for industrial applications. Provides excellent heat transfer with minimal dimensions.',
                'price_usd': 15000,
                'is_featured': True,
                'specs': [
                    ('Потужність', 'Power', 'Мощность', '100', 'кВт'),
                    ('Тиск', 'Pressure', 'Давление', '16', 'бар'),
                    ('Температура', 'Temperature', 'Температура', '180', '°C'),
                    ('Матеріал', 'Material', 'Материал', '316L', ''),
                ],
                'advantages': [
                    ('Висока ефективність', 'High efficiency', 'Высокая эффективность', 'Коефіцієнт теплопередачі до 95%'),
                    ('Компактність', 'Compact design', 'Компактность', 'Займає мінімум простору'),
                    ('Надійність', 'Reliability', 'Надежность', 'Довгий термін служби'),
                    ('Сервіс', 'Service', 'Сервис', 'Легке обслуговування'),
                ]
            },
            {
                'category_slug': 'heat-exchangers',
                'name_uk': 'Кожухотрубний теплообмінник КТ-200',
                'name_ru': 'Кожухотрубный теплообменник КТ-200',
                'name_en': 'Shell and Tube Heat Exchanger ST-200',
                'slug': 'shell-tube-heat-exchanger-st-200',
                'short_description_uk': 'Потужний кожухотрубний теплообмінник для важких умов експлуатації',
                'short_description_ru': 'Мощный кожухотрубный теплообменник для тяжелых условий эксплуатации',
                'short_description_en': 'Powerful shell and tube heat exchanger for heavy duty applications',
                'description_uk': 'КТ-200 призначений для роботи в найважчих промислових умовах. Витримує високі тиски та температури.',
                'description_ru': 'КТ-200 предназначен для работы в самых тяжелых промышленных условиях. Выдерживает высокие давления и температуры.',
                'description_en': 'ST-200 is designed for the most demanding industrial conditions. Withstands high pressures and temperatures.',
                'price_usd': 25000,
                'is_featured': False,
            },
            {
                'category_slug': 'heat-exchangers',
                'name_uk': 'Спіральний теплообмінник СТ-150',
                'name_ru': 'Спиральный теплообменник СТ-150',
                'name_en': 'Spiral Heat Exchanger SP-150',
                'slug': 'spiral-heat-exchanger-sp-150',
                'short_description_uk': 'Спіральний теплообмінник для в\'язких та забруднених рідин',
                'short_description_ru': 'Спиральный теплообменник для вязких и загрязненных жидкостей',
                'short_description_en': 'Spiral heat exchanger for viscous and contaminated liquids',
                'description_uk': 'СТ-150 ідеально підходить для роботи з в\'язкими рідинами та середовищами з високим вмістом твердих частинок.',
                'description_ru': 'СТ-150 идеально подходит для работы с вязкими жидкостями и средами с высоким содержанием твердых частиц.',
                'description_en': 'SP-150 is perfect for handling viscous liquids and media with high solid content.',
                'price_usd': 18000,
                'is_featured': True,
            },
            
            # Кондиціонери (3 продукти)
            {
                'category_slug': 'air-conditioners',
                'name_uk': 'Промисловий кондиціонер АС-500',
                'name_ru': 'Промышленный кондиционер АС-500',
                'name_en': 'Industrial Air Conditioner AC-500',
                'slug': 'industrial-air-conditioner-ac-500',
                'short_description_uk': 'Потужна система кондиціонування для великих промислових приміщень',
                'short_description_ru': 'Мощная система кондиционирования для больших промышленных помещений',
                'short_description_en': 'Powerful conditioning system for large industrial spaces',
                'description_uk': 'АС-500 забезпечує ефективне кондиціонування великих промислових об\'єктів з автоматичним контролем температури та вологості.',
                'description_ru': 'АС-500 обеспечивает эффективное кондиционирование больших промышленных объектов с автоматическим контролем температуры и влажности.',
                'description_en': 'AC-500 provides efficient conditioning of large industrial facilities with automatic temperature and humidity control.',
                'price_usd': 35000,
                'is_featured': True,
            },
            {
                'category_slug': 'air-conditioners',
                'name_uk': 'Прецизійний кондиціонер ПК-100',
                'name_ru': 'Прецизионный кондиционер ПК-100',
                'name_en': 'Precision Air Conditioner PC-100',
                'slug': 'precision-air-conditioner-pc-100',
                'short_description_uk': 'Високоточна система підтримки мікроклімату',
                'short_description_ru': 'Высокоточная система поддержания микроклимата',
                'short_description_en': 'High-precision microclimate maintenance system',
                'description_uk': 'ПК-100 призначений для серверних, лабораторій та інших приміщень, що потребують точного контролю температури.',
                'description_ru': 'ПК-100 предназначен для серверных, лабораторий и других помещений, требующих точного контроля температуры.',
                'description_en': 'PC-100 is designed for server rooms, laboratories and other spaces requiring precise temperature control.',
                'price_usd': 12000,
                'is_featured': False,
            },
            
            # Вентиляційне обладнання (3 продукти)  
            {
                'category_slug': 'ventilation-equipment',
                'name_uk': 'Промисловий вентилятор ВП-1000',
                'name_ru': 'Промышленный вентилятор ВП-1000',
                'name_en': 'Industrial Fan IF-1000',
                'slug': 'industrial-fan-if-1000',
                'short_description_uk': 'Високопродуктивний осьовий вентилятор для промислової вентиляції',
                'short_description_ru': 'Высокопроизводительный осевой вентилятор для промышленной вентиляции',
                'short_description_en': 'High-performance axial fan for industrial ventilation',
                'description_uk': 'ВП-1000 забезпечує потужний повітряний потік для ефективної вентиляції великих промислових приміщень.',
                'description_ru': 'ВП-1000 обеспечивает мощный воздушный поток для эффективной вентиляции больших промышленных помещений.',
                'description_en': 'IF-1000 provides powerful airflow for efficient ventilation of large industrial spaces.',
                'price_usd': 8000,
                'is_featured': True,
            },
            {
                'category_slug': 'ventilation-equipment',
                'name_uk': 'Рекуператор РК-500',
                'name_ru': 'Рекуператор РК-500',
                'name_en': 'Heat Recovery Unit HR-500',
                'slug': 'heat-recovery-unit-hr-500',
                'short_description_uk': 'Енергоефективна система рекуперації тепла',
                'short_description_ru': 'Энергоэффективная система рекуперации тепла',
                'short_description_en': 'Energy-efficient heat recovery system',
                'description_uk': 'РК-500 дозволяє зменшити енергоспоживання на 70% за рахунок рекуперації тепла відпрацьованого повітря.',
                'description_ru': 'РК-500 позволяет снизить энергопотребление на 70% за счет рекуперации тепла отработанного воздуха.',
                'description_en': 'HR-500 reduces energy consumption by 70% through exhaust air heat recovery.',
                'price_usd': 22000,
                'is_featured': False,
            },
        ]
        
        for data in products_data:
            # Знаходимо категорію
            try:
                category = Category.objects.get(slug=data['category_slug'])
            except Category.DoesNotExist:
                self.stdout.write(f'❌ Категорія {data["category_slug"]} не знайдена')
                continue
            
            # Створюємо продукт
            product_data = {k: v for k, v in data.items() if k not in ['category_slug', 'specs', 'advantages']}
            product_data['category'] = category
            
            product, created = Product.objects.get_or_create(
                slug=data['slug'],
                defaults=product_data
            )
            
            if created:
                self.stdout.write(f'✅ Створено продукт: {product.name_uk}')
                
                # Додаємо характеристики, якщо вони є
                if 'specs' in data:
                    for spec_data in data['specs']:
                        ProductSpec.objects.create(
                            product=product,
                            name_uk=spec_data[0],
                            name_en=spec_data[1],
                            name_ru=spec_data[2],
                            value=spec_data[3],
                            unit=spec_data[4],
                        )
                
                # Додаємо переваги, якщо вони є
                if 'advantages' in data:
                    for i, adv_data in enumerate(data['advantages']):
                        ProductAdvantage.objects.create(
                            product=product,
                            title_uk=adv_data[0],
                            title_en=adv_data[1],
                            title_ru=adv_data[2],
                            description_uk=adv_data[3],
                            description_ru=adv_data[3],
                            description_en=adv_data[3],
                            order=i,
                            icon='fas fa-check'
                        )
                        
            else:
                self.stdout.write(f'⚠️  Продукт вже існує: {product.name_uk}')
