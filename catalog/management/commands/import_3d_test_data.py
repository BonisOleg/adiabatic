from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from catalog.models import Product, ProductGallery, Category
from PIL import Image
import io
import os


class Command(BaseCommand):
    help = 'Create test products with 3D gallery items'

    def handle(self, *args, **options):
        """Створити тестові продукти з 3D файлами для демонстрації"""
        
        # Створити категорію, якщо не існує
        category, created = Category.objects.get_or_create(
            slug='test-heat-exchangers',
            defaults={
                'name_uk': 'Тестові теплообмінники',
                'name_ru': 'Тестовые теплообменники',
                'name_en': 'Test Heat Exchangers',
                'description_uk': 'Тестові продукти для демонстрації 3D функціональності',
                'description_ru': 'Тестовые продукты для демонстрации 3D функциональности',
                'description_en': 'Test products for 3D functionality demonstration',
                'icon': 'fas fa-cube',
                'is_published': True
            }
        )
        
        if created:
            self.stdout.write(f"✅ Створено категорію: {category.name_uk}")
        else:
            self.stdout.write(f"📁 Використовується існуюча категорія: {category.name_uk}")
        
        # Тестові продукти
        test_products = [
            {
                'slug': 'plate-heat-exchanger-3d',
                'name_uk': 'Пластинчатий теплообмінник FP09-77',
                'name_ru': 'Пластинчатый теплообменник FP09-77',
                'name_en': 'Plate Heat Exchanger FP09-77',
                'short_description_uk': 'Високоефективний пластинчатий теплообмінник для промислових застосувань',
                'short_description_ru': 'Высокоэффективный пластинчатый теплообменник для промышленных применений',
                'short_description_en': 'High-efficiency plate heat exchanger for industrial applications',
                'description_uk': 'Професійний пластинчатий теплообмінник з нержавіючої сталі. Забезпечує високу ефективність теплопередачі та надійність в експлуатації.',
                'description_ru': 'Профессиональный пластинчатый теплообменник из нержавеющей стали. Обеспечивает высокую эффективность теплопередачи и надежность в эксплуатации.',
                'description_en': 'Professional stainless steel plate heat exchanger. Provides high heat transfer efficiency and operational reliability.',
                'power_kw': 50.5,
                'max_pressure_bar': 16.0,
                'max_temperature_c': 180.0,
                'price_usd': 2500.00,
                'files': [
                    {'type': '3D_MODEL', 'filename': 'FP09-77-1-NH.stp'},
                    {'type': 'IMAGE', 'filename': 'plate_exchanger_1.jpg'},
                    {'type': 'IMAGE', 'filename': 'plate_exchanger_2.jpg'},
                ]
            },
            {
                'slug': 'shell-tube-exchanger-3d',
                'name_uk': 'Кожухотрубний теплообмінник 569kW',
                'name_ru': 'Кожухотрубный теплообменник 569kW',
                'name_en': 'Shell & Tube Heat Exchanger 569kW',
                'short_description_uk': 'Потужний кожухотрубний теплообмінник для великих промислових систем',
                'short_description_ru': 'Мощный кожухотрубный теплообменник для больших промышленных систем',
                'short_description_en': 'Powerful shell & tube heat exchanger for large industrial systems',
                'description_uk': 'Високопродуктивний кожухотрубний теплообмінник потужністю 569 кВт. Призначений для роботи з великими об\'ємами рідин при високих температурах.',
                'description_ru': 'Высокопроизводительный кожухотрубный теплообменник мощностью 569 кВт. Предназначен для работы с большими объемами жидкостей при высоких температурах.',
                'description_en': 'High-performance shell & tube heat exchanger with 569 kW capacity. Designed for handling large fluid volumes at high temperatures.',
                'power_kw': 569.0,
                'max_pressure_bar': 25.0,
                'max_temperature_c': 300.0,
                'price_usd': 15000.00,
                'files': [
                    {'type': '3D_MODEL', 'filename': 'Heating_Unit_569_kW.stp'},
                    {'type': 'IMAGE', 'filename': 'shell_tube_1.jpg'},
                    {'type': 'TECHNICAL_DRAWING', 'filename': 'shell_tube_drawing.dwg'},
                ]
            },
            {
                'slug': 'compact-heat-exchanger-3d',
                'name_uk': 'Компактний теплообмінник',
                'name_ru': 'Компактный теплообменник',
                'name_en': 'Compact Heat Exchanger',
                'short_description_uk': 'Економічне рішення для малих та середніх систем',
                'short_description_ru': 'Экономичное решение для малых и средних систем',
                'short_description_en': 'Cost-effective solution for small to medium systems',
                'description_uk': 'Компактний та економічний теплообмінник для невеликих систем. Легкий в монтажі та обслуговуванні.',
                'description_ru': 'Компактный и экономичный теплообменник для небольших систем. Легкий в монтаже и обслуживании.',
                'description_en': 'Compact and economical heat exchanger for small systems. Easy to install and maintain.',
                'power_kw': 25.0,
                'max_pressure_bar': 10.0,
                'max_temperature_c': 120.0,
                'price_usd': 1200.00,
                'files': [
                    {'type': 'IMAGE', 'filename': 'compact_1.jpg'},
                    {'type': 'IMAGE', 'filename': 'compact_2.jpg'},
                ]
            }
        ]
        
        # Створити продукти
        for product_data in test_products:
            files_data = product_data.pop('files')
            
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={
                    **product_data,
                    'category': category,
                    'is_published': True,
                    'is_featured': True
                }
            )
            
            if created:
                self.stdout.write(f"✅ Створено продукт: {product.name_uk}")
                
                # Додати файли до галереї
                for i, file_data in enumerate(files_data):
                    gallery_item = self.create_gallery_item(
                        product, 
                        file_data['type'], 
                        file_data['filename'],
                        i
                    )
                    if gallery_item:
                        self.stdout.write(f"   📁 Додано до галереї: {file_data['filename']}")
            else:
                self.stdout.write(f"📦 Продукт вже існує: {product.name_uk}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Завершено! Створено тестові дані для демонстрації 3D функціональності.\n"
                f"   Відвідайте /catalog/ щоб побачити результат!"
            )
        )
    
    def create_gallery_item(self, product, content_type, filename, order):
        """Створити елемент галереї з тестовими даними"""
        
        # Перевірити, чи вже існує
        existing = ProductGallery.objects.filter(
            product=product,
            title_uk__icontains=filename.split('.')[0]
        ).first()
        
        if existing:
            return existing
        
        gallery_item = ProductGallery.objects.create(
            product=product,
            content_type=content_type,
            title_uk=f"{filename.split('.')[0].replace('_', ' ').title()}",
            title_ru=f"{filename.split('.')[0].replace('_', ' ').title()}",
            title_en=f"{filename.split('.')[0].replace('_', ' ').title()}",
            alt_text=f"{content_type} {filename}",
            description=f"Тестовий {content_type.lower()} файл для демонстрації",
            order=order,
            is_downloadable=True,
            file_size=self.get_mock_file_size(content_type)
        )
        
        # Створити тестові файли
        if content_type == 'IMAGE':
            # Створити просте тестове зображення
            test_image = self.create_test_image(filename)
            gallery_item.image.save(filename, test_image, save=False)
        
        elif content_type == '3D_MODEL':
            # Створити простий тестовий 3D файл
            test_3d_content = self.create_test_3d_content(filename)
            gallery_item.file_3d.save(filename, test_3d_content, save=False)
            
            # Створити превью зображення для 3D моделі
            preview_image = self.create_test_image(f"preview_{filename}.jpg")
            gallery_item.preview_image.save(f"preview_{filename}.jpg", preview_image, save=False)
        
        elif content_type == 'TECHNICAL_DRAWING':
            # Створити тестовий файл креслення
            test_drawing = self.create_test_drawing_content(filename)
            gallery_item.file_3d.save(filename, test_drawing, save=False)
        
        gallery_item.save()
        return gallery_item
    
    def create_test_image(self, filename):
        """Створити просте тестове зображення"""
        # Створити простий градієнт як тестове зображення
        img = Image.new('RGB', (400, 300), color='lightblue')
        
        # Додати текст (спрощений варіант без PIL.ImageDraw)
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)
        
        return ContentFile(buffer.getvalue(), name=filename)
    
    def create_test_3d_content(self, filename):
        """Створити простий тестовий 3D файл"""
        # Простий STEP файл header (мінімальний)
        step_content = """ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('Test 3D Model'), '2;1');
FILE_NAME('""" + filename + """', '2024-01-01T12:00:00', ('Test'), ('Test Organization'), 'Test CAD System', 'Test CAD System', '');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));
ENDSEC;

DATA;
#1 = APPLICATION_CONTEXT('automotive_design') ;
#2 = APPLICATION_PROTOCOL_DEFINITION('automotive_design','','AP214',#1) ;
ENDSEC;

END-ISO-10303-21;
"""
        return ContentFile(step_content.encode('utf-8'), name=filename)
    
    def create_test_drawing_content(self, filename):
        """Створити простий тестовий файл креслення"""
        # Простий DWG header placeholder
        dwg_content = b"Test DWG file content - placeholder for demonstration"
        return ContentFile(dwg_content, name=filename)
    
    def get_mock_file_size(self, content_type):
        """Отримати розмір файлу для різних типів"""
        sizes = {
            'IMAGE': '250 KB',
            '3D_MODEL': '1.2 MB',
            'TECHNICAL_DRAWING': '450 KB'
        }
        return sizes.get(content_type, '100 KB')


