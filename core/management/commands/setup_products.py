from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from catalog.models import Category, Product, ProductSpec, ProductAdvantage


class Command(BaseCommand):
    help = 'Створення категорій та продуктів для каталогу'

    def handle(self, *args, **options):
        self.stdout.write('Створення продуктових даних...')
        
        # Створення категорій
        self.create_categories()
        
        # Створення продуктів
        self.create_products()
        
        self.stdout.write(
            self.style.SUCCESS('Продуктові дані успішно створено!')
        )

    def create_categories(self):
        """Створення категорій продуктів"""
        categories_data = [
            {
                'name_uk': 'Теплообмінники',
                'name_ru': 'Теплообменники',
                'name_en': 'Heat Exchangers',
                'description_uk': 'Професійні теплообмінники для промислових застосувань',
                'description_ru': 'Профессиональные теплообменники для промышленных применений',
                'description_en': 'Professional heat exchangers for industrial applications',
                'slug': 'heat-exchangers',
                'icon': 'fas fa-fire',
                'order': 1,
            },
            {
                'name_uk': 'Енергетичне обладнання',
                'name_ru': 'Энергетическое оборудование',
                'name_en': 'Energy Equipment',
                'description_uk': 'Обладнання для енергетичної галузі',
                'description_ru': 'Оборудование для энергетической отрасли',
                'description_en': 'Equipment for energy industry',
                'slug': 'energy-equipment',
                'icon': 'fas fa-bolt',
                'order': 2,
            },
            {
                'name_uk': 'Спеціальні рішення',
                'name_ru': 'Специальные решения',
                'name_en': 'Special Solutions',
                'description_uk': 'Індивідуальні рішення для складних завдань',
                'description_ru': 'Индивидуальные решения для сложных задач',
                'description_en': 'Individual solutions for complex tasks',
                'slug': 'special-solutions',
                'icon': 'fas fa-cogs',
                'order': 3,
            },
        ]
        
        for cat_data in categories_data:
            Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
        
        self.stdout.write('Категорії продуктів створено')

    def create_products(self):
        """Створення 10 продуктів"""
        # Отримуємо категорії
        heat_exchangers = Category.objects.get(slug='heat-exchangers')
        energy_equipment = Category.objects.get(slug='energy-equipment')
        special_solutions = Category.objects.get(slug='special-solutions')
        
        products_data = [
            # Теплообмінники (4 продукти)
            {
                'category': heat_exchangers,
                'name_uk': 'Пластинчастий теплообмінник PHE-100',
                'name_ru': 'Пластинчатый теплообменник PHE-100',
                'name_en': 'Plate Heat Exchanger PHE-100',
                'slug': 'phe-100',
                'short_description_uk': 'Високоефективний пластинчастий теплообмінник для промислового використання',
                'short_description_ru': 'Высокоэффективный пластинчатый теплообменник для промышленного использования',
                'short_description_en': 'High-efficiency plate heat exchanger for industrial use',
                'description_uk': 'Пластинчастий теплообмінник PHE-100 призначений для ефективного теплообміну в промислових системах. Забезпечує високу продуктивність та надійність.',
                'description_ru': 'Пластинчатый теплообменник PHE-100 предназначен для эффективного теплообмена в промышленных системах. Обеспечивает высокую производительность и надежность.',
                'description_en': 'Plate heat exchanger PHE-100 is designed for efficient heat transfer in industrial systems. Provides high performance and reliability.',
                'application_type': 'INDUSTRIAL',
                'fluid_type': 'WATER',
                'power_kw': 100.0,
                'max_pressure_bar': 16.0,
                'max_temperature_c': 180.0,
                'material_shell': 'Нержавіюча сталь 316L',
                'material_tubes': 'Нержавіюча сталь 316L',
                'standards': 'ASME, DIN, GOST',
                'is_featured': True,
            },
            {
                'category': heat_exchangers,
                'name_uk': 'Трубчастий теплообмінник THE-200',
                'name_ru': 'Трубчатый теплообменник THE-200',
                'name_en': 'Tube Heat Exchanger THE-200',
                'slug': 'the-200',
                'short_description_uk': 'Надійний трубчастий теплообмінник для важких умов експлуатації',
                'short_description_ru': 'Надежный трубчатый теплообменник для тяжелых условий эксплуатации',
                'short_description_en': 'Reliable tube heat exchanger for heavy-duty operation',
                'description_uk': 'Трубчастий теплообмінник THE-200 ідеально підходить для роботи в агресивних середовищах та при високих температурах.',
                'description_ru': 'Трубчатый теплообменник THE-200 идеально подходит для работы в агрессивных средах и при высоких температурах.',
                'description_en': 'Tube heat exchanger THE-200 is perfect for operation in aggressive environments and high temperatures.',
                'application_type': 'INDUSTRIAL',
                'fluid_type': 'OIL',
                'power_kw': 200.0,
                'max_pressure_bar': 25.0,
                'max_temperature_c': 300.0,
                'material_shell': 'Вуглецева сталь',
                'material_tubes': 'Нержавіюча сталь 321',
                'standards': 'ASME, API',
                'is_featured': True,
            },
            {
                'category': heat_exchangers,
                'name_uk': 'Паяний теплообмінник BHE-50',
                'name_ru': 'Паяный теплообменник BHE-50',
                'name_en': 'Brazed Heat Exchanger BHE-50',
                'slug': 'bhe-50',
                'short_description_uk': 'Компактний паяний теплообмінник для систем кондиціонування',
                'short_description_ru': 'Компактный паяный теплообменник для систем кондиционирования',
                'short_description_en': 'Compact brazed heat exchanger for air conditioning systems',
                'description_uk': 'Паяний теплообмінник BHE-50 забезпечує максимальну ефективність в мінімальному обсязі.',
                'description_ru': 'Паяный теплообменник BHE-50 обеспечивает максимальную эффективность в минимальном объеме.',
                'description_en': 'Brazed heat exchanger BHE-50 provides maximum efficiency in minimal volume.',
                'application_type': 'HVAC',
                'fluid_type': 'REFRIGERANT',
                'power_kw': 50.0,
                'max_pressure_bar': 30.0,
                'max_temperature_c': 200.0,
                'material_shell': 'Нержавіюча сталь',
                'material_tubes': 'Мідь',
                'standards': 'EN, AHRI',
                'is_featured': False,
            },
            {
                'category': heat_exchangers,
                'name_uk': 'Спіральний теплообмінник SHE-150',
                'name_ru': 'Спиральный теплообменник SHE-150',
                'name_en': 'Spiral Heat Exchanger SHE-150',
                'slug': 'she-150',
                'short_description_uk': 'Інноваційний спіральний теплообмінник для в\'язких рідин',
                'short_description_ru': 'Инновационный спиральный теплообменник для вязких жидкостей',
                'short_description_en': 'Innovative spiral heat exchanger for viscous fluids',
                'description_uk': 'Спіральний теплообмінник SHE-150 ідеально підходить для роботи з в\'язкими та забруднюючими рідинами.',
                'description_ru': 'Спиральный теплообменник SHE-150 идеально подходит для работы с вязкими и загрязняющими жидкостями.',
                'description_en': 'Spiral heat exchanger SHE-150 is perfect for working with viscous and fouling fluids.',
                'application_type': 'FOOD',
                'fluid_type': 'CHEMICAL',
                'power_kw': 150.0,
                'max_pressure_bar': 16.0,
                'max_temperature_c': 250.0,
                'material_shell': 'Нержавіюча сталь 316L',
                'material_tubes': 'Нержавіюча сталь 316L',
                'standards': 'ASME, 3A',
                'is_featured': False,
            },
            
            # Енергетичне обладнання (3 продукти)
            {
                'category': energy_equipment,
                'name_uk': 'Котел-утилізатор КУ-500',
                'name_ru': 'Котел-утилизатор КУ-500',
                'name_en': 'Heat Recovery Steam Generator HRSG-500',
                'slug': 'hrsg-500',
                'short_description_uk': 'Потужний котел-утилізатор для електростанцій',
                'short_description_ru': 'Мощный котел-утилизатор для электростанций',
                'short_description_en': 'Powerful heat recovery steam generator for power plants',
                'description_uk': 'Котел-утилізатор КУ-500 призначений для використання теплоти відхідних газів газових турбін.',
                'description_ru': 'Котел-утилизатор КУ-500 предназначен для использования теплоты отходящих газов газовых турбин.',
                'description_en': 'HRSG-500 is designed to utilize heat from gas turbine exhaust gases.',
                'application_type': 'ENERGY',
                'fluid_type': 'STEAM',
                'power_kw': 500.0,
                'max_pressure_bar': 80.0,
                'max_temperature_c': 550.0,
                'material_shell': 'Вуглецева сталь',
                'material_tubes': 'Легована сталь',
                'standards': 'ASME, EN',
                'is_featured': True,
            },
            {
                'category': energy_equipment,
                'name_uk': 'Повітряний охолоджувач АВО-300',
                'name_ru': 'Воздушный охладитель АВО-300',
                'name_en': 'Air Cooler ACO-300',
                'slug': 'aco-300',
                'short_description_uk': 'Ефективний повітряний охолоджувач для нафтогазової галузі',
                'short_description_ru': 'Эффективный воздушный охладитель для нефтегазовой отрасли',
                'short_description_en': 'Efficient air cooler for oil and gas industry',
                'description_uk': 'Повітряний охолоджувач АВО-300 забезпечує надійне охолодження в умовах обмеженого водопостачання.',
                'description_ru': 'Воздушный охладитель АВО-300 обеспечивает надежное охлаждение в условиях ограниченного водоснабжения.',
                'description_en': 'Air cooler ACO-300 provides reliable cooling under limited water supply conditions.',
                'application_type': 'OIL_GAS',
                'fluid_type': 'OIL',
                'power_kw': 300.0,
                'max_pressure_bar': 40.0,
                'max_temperature_c': 200.0,
                'material_shell': 'Вуглецева сталь',
                'material_tubes': 'Алюміній',
                'standards': 'API, ASME',
                'is_featured': False,
            },
            {
                'category': energy_equipment,
                'name_uk': 'Конденсатор КНД-400',
                'name_ru': 'Конденсатор КНД-400',
                'name_en': 'Condenser CND-400',
                'slug': 'cnd-400',
                'short_description_uk': 'Високопродуктивний конденсатор для теплових електростанцій',
                'short_description_ru': 'Высокопроизводительный конденсатор для тепловых электростанций',
                'short_description_en': 'High-performance condenser for thermal power plants',
                'description_uk': 'Конденсатор КНД-400 забезпечує ефективну конденсацію пари в енергетичних установках.',
                'description_ru': 'Конденсатор КНД-400 обеспечивает эффективную конденсацию пара в энергетических установках.',
                'description_en': 'Condenser CND-400 provides efficient steam condensation in power plants.',
                'application_type': 'ENERGY',
                'fluid_type': 'STEAM',
                'power_kw': 400.0,
                'max_pressure_bar': 0.1,
                'max_temperature_c': 60.0,
                'material_shell': 'Вуглецева сталь',
                'material_tubes': 'Титан',
                'standards': 'ASME, DIN',
                'is_featured': False,
            },
            
            # Спеціальні рішення (3 продукти)
            {
                'category': special_solutions,
                'name_uk': 'Реактор РТ-1000',
                'name_ru': 'Реактор РТ-1000',
                'name_en': 'Reactor RT-1000',
                'slug': 'rt-1000',
                'short_description_uk': 'Спеціалізований реактор для хімічної промисловості',
                'short_description_ru': 'Специализированный реактор для химической промышленности',
                'short_description_en': 'Specialized reactor for chemical industry',
                'description_uk': 'Реактор РТ-1000 призначений для проведення складних хімічних процесів при високих температурах та тисках.',
                'description_ru': 'Реактор РТ-1000 предназначен для проведения сложных химических процессов при высоких температурах и давлениях.',
                'description_en': 'Reactor RT-1000 is designed for complex chemical processes at high temperatures and pressures.',
                'application_type': 'CUSTOM',
                'fluid_type': 'CHEMICAL',
                'power_kw': 1000.0,
                'max_pressure_bar': 100.0,
                'max_temperature_c': 400.0,
                'material_shell': 'Спеціальна сталь',
                'material_tubes': 'Хастеллой',
                'standards': 'ASME VIII, PED',
                'is_featured': True,
            },
            {
                'category': special_solutions,
                'name_uk': 'Випарна установка ВУ-250',
                'name_ru': 'Выпарная установка ВУ-250',
                'name_en': 'Evaporator EVP-250',
                'slug': 'evp-250',
                'short_description_uk': 'Багатокорпусна випарна установка для концентрування розчинів',
                'short_description_ru': 'Многокорпусная выпарная установка для концентрирования растворов',
                'short_description_en': 'Multi-effect evaporator for solution concentration',
                'description_uk': 'Випарна установка ВУ-250 забезпечує ефективне концентрування розчинів з мінімальними енерговитратами.',
                'description_ru': 'Выпарная установка ВУ-250 обеспечивает эффективное концентрирование растворов с минимальными энергозатратами.',
                'description_en': 'Evaporator EVP-250 provides efficient solution concentration with minimal energy consumption.',
                'application_type': 'FOOD',
                'fluid_type': 'STEAM',
                'power_kw': 250.0,
                'max_pressure_bar': 6.0,
                'max_temperature_c': 160.0,
                'material_shell': 'Нержавіюча сталь 316L',
                'material_tubes': 'Нержавіюча сталь 316L',
                'standards': 'ASME, 3A, EHEDG',
                'is_featured': False,
            },
            {
                'category': special_solutions,
                'name_uk': 'Морська опріснювальна установка МОУ-100',
                'name_ru': 'Морская опреснительная установка МОУ-100',
                'name_en': 'Marine Desalination Unit MDU-100',
                'slug': 'mdu-100',
                'short_description_uk': 'Компактна опріснювальна установка для морських суден',
                'short_description_ru': 'Компактная опреснительная установка для морских судов',
                'short_description_en': 'Compact desalination unit for marine vessels',
                'description_uk': 'Морська опріснювальна установка МОУ-100 забезпечує автономне водопостачання на морських суднах.',
                'description_ru': 'Морская опреснительная установка МОУ-100 обеспечивает автономное водоснабжение на морских судах.',
                'description_en': 'Marine desalination unit MDU-100 provides autonomous water supply on marine vessels.',
                'application_type': 'MARINE',
                'fluid_type': 'WATER',
                'power_kw': 100.0,
                'max_pressure_bar': 70.0,
                'max_temperature_c': 80.0,
                'material_shell': 'Морська нержавіюча сталь',
                'material_tubes': 'Титан',
                'standards': 'IMO, SOLAS',
                'is_featured': False,
            },
        ]
        
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )
            
            if created:
                # Додаємо технічні характеристики
                self.create_product_specs(product)
                # Додаємо переваги
                self.create_product_advantages(product)
        
        self.stdout.write('Продукти створено')

    def create_product_specs(self, product):
        """Створення технічних характеристик для продукту"""
        base_specs = [
            {
                'name_uk': 'Потужність',
                'name_ru': 'Мощность', 
                'name_en': 'Power',
                'value': f'{product.power_kw}',
                'unit': 'кВт',
                'order': 1,
            },
            {
                'name_uk': 'Максимальний тиск',
                'name_ru': 'Максимальное давление',
                'name_en': 'Maximum pressure', 
                'value': f'{product.max_pressure_bar}',
                'unit': 'бар',
                'order': 2,
            },
            {
                'name_uk': 'Максимальна температура',
                'name_ru': 'Максимальная температура',
                'name_en': 'Maximum temperature',
                'value': f'{product.max_temperature_c}',
                'unit': '°C',
                'order': 3,
            },
            {
                'name_uk': 'Матеріал корпусу',
                'name_ru': 'Материал корпуса', 
                'name_en': 'Shell material',
                'value': product.material_shell,
                'unit': '',
                'order': 4,
            },
            {
                'name_uk': 'Стандарти',
                'name_ru': 'Стандарты',
                'name_en': 'Standards', 
                'value': product.standards,
                'unit': '',
                'order': 5,
            },
        ]
        
        for spec_data in base_specs:
            ProductSpec.objects.get_or_create(
                product=product,
                name_uk=spec_data['name_uk'],
                defaults=spec_data
            )

    def create_product_advantages(self, product):
        """Створення переваг продукту"""
        advantages_data = [
            {
                'title_uk': 'Висока ефективність',
                'title_ru': 'Высокая эффективность',
                'title_en': 'High efficiency',
                'description_uk': 'Максимальна теплопередача при мінімальних втратах',
                'description_ru': 'Максимальная теплопередача при минимальных потерях',
                'description_en': 'Maximum heat transfer with minimal losses',
                'icon': 'fas fa-chart-line',
                'order': 1,
            },
            {
                'title_uk': 'Надійність',
                'title_ru': 'Надежность',
                'title_en': 'Reliability',
                'description_uk': 'Довгий термін служби та стабільна робота',
                'description_ru': 'Долгий срок службы и стабильная работа', 
                'description_en': 'Long service life and stable operation',
                'icon': 'fas fa-shield-alt',
                'order': 2,
            },
            {
                'title_uk': 'Простота обслуговування',
                'title_ru': 'Простота обслуживания',
                'title_en': 'Easy maintenance',
                'description_uk': 'Зручний доступ до всіх вузлів для технічного обслуговування',
                'description_ru': 'Удобный доступ ко всем узлам для технического обслуживания',
                'description_en': 'Convenient access to all components for maintenance',
                'icon': 'fas fa-tools',
                'order': 3,
            },
        ]
        
        for advantage_data in advantages_data:
            ProductAdvantage.objects.get_or_create(
                product=product,
                title_uk=advantage_data['title_uk'],
                defaults=advantage_data
            )
