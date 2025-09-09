from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from catalog.models import Product, ProductGallery, Category
from PIL import Image
import os
import shutil
from pathlib import Path


class Command(BaseCommand):
    help = 'Import real 3D products from static/images/3D/ directory'

    def add_arguments(self, parser):
        parser.add_argument(
            '--copy-files',
            action='store_true',
            help='Copy files to media directory for production use',
        )

    def handle(self, *args, **options):
        """Імпорт реальних 3D файлів з папки static/images/3D/"""
        
        self.copy_files = options.get('copy_files', False)
        
        # Базовий шлях до 3D файлів
        base_3d_path = Path(settings.BASE_DIR) / 'static' / 'images' / '3D'
        
        if not base_3d_path.exists():
            self.stdout.write(
                self.style.ERROR(f"❌ Папка {base_3d_path} не знайдена!")
            )
            return
        
        # Mapping категорій
        categories_mapping = {
            'Нестандарт': {
                'code': 'CUSTOM',
                'name_uk': 'Нестандартні теплообмінники',
                'name_ru': 'Нестандартные теплообменники',
                'name_en': 'Custom Heat Exchangers',
                'description_uk': 'Спеціальні рішення для унікальних промислових задач',
                'description_ru': 'Специальные решения для уникальных промышленных задач',
                'description_en': 'Special solutions for unique industrial applications',
                'icon': 'fas fa-cogs'
            },
            'Трубчатые': {
                'code': 'SHELL_TUBE',
                'name_uk': 'Кожухотрубні теплообмінники',
                'name_ru': 'Кожухотрубные теплообменники',
                'name_en': 'Shell & Tube Heat Exchangers',
                'description_uk': 'Надійні кожухотрубні теплообмінники для промислових процесів',
                'description_ru': 'Надежные кожухотрубные теплообменники для промышленных процессов',
                'description_en': 'Reliable shell & tube heat exchangers for industrial processes',
                'icon': 'fas fa-industry'
            },
            'Паяные': {
                'code': 'BRAZED',
                'name_uk': 'Паяні теплообмінники',
                'name_ru': 'Паяные теплообменники', 
                'name_en': 'Brazed Heat Exchangers',
                'description_uk': 'Компактні паяні теплообмінники високої ефективності',
                'description_ru': 'Компактные паяные теплообменники высокой эффективности',
                'description_en': 'Compact high-efficiency brazed heat exchangers',
                'icon': 'fas fa-fire'
            },
            'Пластинчатые': {
                'code': 'PLATE',
                'name_uk': 'Пластинчаті теплообмінники',
                'name_ru': 'Пластинчатые теплообменники',
                'name_en': 'Plate Heat Exchangers',
                'description_uk': 'Ефективні пластинчаті теплообмінники для різних застосувань',
                'description_ru': 'Эффективные пластинчатые теплообменники для различных применений',
                'description_en': 'Efficient plate heat exchangers for various applications',
                'icon': 'fas fa-layer-group'
            }
        }
        
        total_products = 0
        total_files = 0
        
        # Обробка кожної категорії
        for category_folder, category_info in categories_mapping.items():
            category_path = base_3d_path / category_folder
            
            if not category_path.exists():
                self.stdout.write(f"⚠️  Папка {category_folder} не знайдена, пропускаємо")
                continue
            
            # Створення або отримання категорії
            category, created = Category.objects.get_or_create(
                slug=category_info['code'].lower().replace('_', '-'),
                defaults={
                    **{k: v for k, v in category_info.items() if k != 'code'},
                    'is_published': True,
                    'order': len(categories_mapping) - list(categories_mapping.keys()).index(category_folder)
                }
            )
            
            if created:
                self.stdout.write(f"✅ Створено категорію: {category.name_uk}")
            
            # Обробка нумерованих папок в категорії
            numbered_dirs = [d for d in category_path.iterdir() if d.is_dir() and d.name.isdigit()]
            numbered_dirs.sort(key=lambda x: int(x.name))
            
            for product_dir in numbered_dirs:
                product_number = int(product_dir.name)
                
                # Створення продукту
                product = self.create_product(category, category_folder, product_number, product_dir)
                if product:
                    total_products += 1
                    
                    # Додавання файлів до галереї
                    files_added = self.add_files_to_gallery(product, product_dir, category_folder, product_number)
                    total_files += files_added
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Імпорт завершено!\n"
                f"   📦 Продуктів створено: {total_products}\n"
                f"   📁 Файлів додано: {total_files}\n"
                f"   🚀 Відвідайте /catalog/ щоб побачити результат!"
            )
        )
        
        if self.copy_files:
            self.stdout.write(
                self.style.SUCCESS(
                    "📋 Файли скопійовані до media/ для продакшену"
                )
            )

    def create_product(self, category, category_folder, product_number, product_dir):
        """Створити продукт на основі папки"""
        
        # Генерація назви продукту
        product_names = self.generate_product_names(category_folder, product_number, product_dir)
        
        slug = f"{category.slug}-{product_number}"
        
        # Перевірка чи продукт вже існує
        existing_product = Product.objects.filter(slug=slug).first()
        if existing_product:
            self.stdout.write(f"📦 Продукт вже існує: {existing_product.name_uk}")
            return existing_product
        
        # Створення нового продукту
        product = Product.objects.create(
            category=category,
            slug=slug,
            **product_names,
            power_kw=self.estimate_power(product_dir),
            max_pressure_bar=self.estimate_pressure(category_folder),
            max_temperature_c=self.estimate_temperature(category_folder),
            application_type=self.get_application_type(category_folder),
            is_published=True,
            is_featured=product_number <= 3  # Перші 3 в кожній категорії як featured
        )
        
        self.stdout.write(f"✅ Створено продукт: {product.name_uk}")
        return product
    
    def generate_product_names(self, category_folder, product_number, product_dir):
        """Генерація назв продукту на основі файлів та категорії"""
        
        # Базові назви категорій
        base_names = {
            'Нестандарт': {
                'uk': 'Нестандартний теплообмінник',
                'ru': 'Нестандартный теплообменник',
                'en': 'Custom Heat Exchanger'
            },
            'Трубчатые': {
                'uk': 'Кожухотрубний теплообмінник',
                'ru': 'Кожухотрубный теплообменник',
                'en': 'Shell & Tube Heat Exchanger'
            },
            'Паяные': {
                'uk': 'Паяний теплообмінник',
                'ru': 'Паяный теплообменник',
                'en': 'Brazed Heat Exchanger'
            },
            'Пластинчатые': {
                'uk': 'Пластинчатий теплообмінник',
                'ru': 'Пластинчатый теплообменник',
                'en': 'Plate Heat Exchanger'
            }
        }
        
        # Спробуємо знайти специфічну назву з файлів
        specific_name = self.extract_name_from_files(product_dir)
        base = base_names.get(category_folder, base_names['Нестандарт'])
        
        if specific_name:
            name_suffix = f" {specific_name}"
        else:
            name_suffix = f" №{product_number}"
        
        return {
            'name_uk': base['uk'] + name_suffix,
            'name_ru': base['ru'] + name_suffix,
            'name_en': base['en'] + name_suffix,
            'short_description_uk': f"Професійний {base['uk'].lower()} для промислових застосувань",
            'short_description_ru': f"Профессиональный {base['ru'].lower()} для промышленных применений",
            'short_description_en': f"Professional {base['en'].lower()} for industrial applications",
            'description_uk': f"Високоякісний {base['uk'].lower()} з оптимальними характеристиками теплопередачі. Підходить для різних промислових процесів та забезпечує надійну роботу в складних умовах експлуатації.",
            'description_ru': f"Высококачественный {base['ru'].lower()} с оптимальными характеристиками теплопередачи. Подходит для различных промышленных процессов и обеспечивает надежную работу в сложных условиях эксплуатации.",
            'description_en': f"High-quality {base['en'].lower()} with optimal heat transfer characteristics. Suitable for various industrial processes and ensures reliable operation in demanding conditions."
        }
    
    def extract_name_from_files(self, product_dir):
        """Витягти специфічну назву з імен файлів"""
        
        # Шукаємо файли з назвами брендів або моделей
        for file_path in product_dir.iterdir():
            if file_path.is_file():
                name = file_path.stem
                
                # Відомі бренди
                if 'Alfa Laval' in name:
                    return name.replace('_', ' ')
                elif 'Funke' in name:
                    return name.replace('_', ' ')
                elif 'FP' in name and any(c.isdigit() for c in name):
                    return name.replace('_', ' ')
                elif any(brand in name.upper() for brand in ['HXC', 'TGB', 'NT_']):
                    return name.replace('_', ' ')
        
        return None
    
    def estimate_power(self, product_dir):
        """Оцінка потужності на основі файлів"""
        for file_path in product_dir.iterdir():
            name = file_path.name.upper()
            if 'KW' in name or 'КВТ' in name:
                # Витягуємо число перед kW
                import re
                match = re.search(r'(\d+)\s*[KК][WВТ]', name)
                if match:
                    return float(match.group(1))
        
        # Дефолтні значення за категоріями
        defaults = {
            1: 25.0, 2: 50.0, 3: 100.0, 4: 150.0, 5: 200.0,
            6: 250.0, 7: 300.0, 8: 400.0, 9: 500.0, 10: 750.0
        }
        return defaults.get(int(product_dir.name), 100.0)
    
    def estimate_pressure(self, category_folder):
        """Оцінка тиску за категорією"""
        pressures = {
            'Пластинчатые': 16.0,
            'Паяные': 30.0,
            'Трубчатые': 25.0,
            'Нестандарт': 20.0
        }
        return pressures.get(category_folder, 16.0)
    
    def estimate_temperature(self, category_folder):
        """Оцінка температури за категорією"""
        temperatures = {
            'Пластинчатые': 180.0,
            'Паяные': 200.0,
            'Трубчатые': 350.0,
            'Нестандарт': 250.0
        }
        return temperatures.get(category_folder, 180.0)
    
    def get_application_type(self, category_folder):
        """Тип застосування за категорією"""
        applications = {
            'Пластинчатые': 'COMPACT',
            'Паяные': 'COMPACT',
            'Трубчатые': 'INDUSTRIAL',
            'Нестандарт': 'CUSTOM'
        }
        return applications.get(category_folder, 'INDUSTRIAL')
    
    def add_files_to_gallery(self, product, product_dir, category_folder, product_number):
        """Додати файли з папки до галереї продукту"""
        
        files_added = 0
        
        # Типи файлів
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        cad_extensions = {'.stp', '.step', '.iges', '.igs', '.dwg', '.dxf'}
        web_3d_extensions = {'.gltf', '.glb', '.obj'}
        archive_extensions = {'.rar', '.zip', '.7z'}
        cad_native_extensions = {'.sldprt', '.sldasm', '.ipt', '.iam', '.prt', '.asm'}
        
        # Сортуємо файли за типом
        files_by_type = {
            'images': [],
            '3d_cad': [],
            '3d_web': [],
            'archives': [],
            'cad_native': []
        }
        
        for file_path in product_dir.iterdir():
            if file_path.is_file():
                ext = file_path.suffix.lower()
                
                if ext in image_extensions:
                    files_by_type['images'].append(file_path)
                elif ext in cad_extensions:
                    files_by_type['3d_cad'].append(file_path)
                elif ext in web_3d_extensions:
                    files_by_type['3d_web'].append(file_path)
                elif ext in archive_extensions:
                    files_by_type['archives'].append(file_path)
                elif ext in cad_native_extensions:
                    files_by_type['cad_native'].append(file_path)
        
        order = 0
        
        # Додаємо зображення спочатку
        for img_path in files_by_type['images']:
            if self.add_gallery_item(product, img_path, 'IMAGE', order):
                files_added += 1
                order += 1
        
        # Додаємо 3D моделі
        for cad_path in files_by_type['3d_cad'] + files_by_type['3d_web'] + files_by_type['cad_native']:
            preview_img = self.find_preview_image(cad_path, files_by_type['images'])
            if self.add_gallery_item(product, cad_path, '3D_MODEL', order, preview_img):
                files_added += 1
                order += 1
        
        # Додаємо креслення (DWG files)
        for file_path in product_dir.iterdir():
            if file_path.suffix.lower() == '.dwg':
                if self.add_gallery_item(product, file_path, 'TECHNICAL_DRAWING', order):
                    files_added += 1
                    order += 1
        
        return files_added
    
    def find_preview_image(self, cad_file, image_files):
        """Знайти найкраще preview зображення для 3D моделі"""
        cad_name = cad_file.stem.lower()
        
        # Спочатку шукаємо файл з схожою назвою
        for img_path in image_files:
            img_name = img_path.stem.lower()
            if img_name in cad_name or cad_name in img_name:
                return img_path
        
        # Якщо не знайшли, повертаємо перше зображення
        return image_files[0] if image_files else None
    
    def add_gallery_item(self, product, file_path, content_type, order, preview_img=None):
        """Додати файл до галереї продукту"""
        
        # Перевіряємо чи вже існує
        existing = ProductGallery.objects.filter(
            product=product,
            alt_text=file_path.name
        ).first()
        
        if existing:
            return False
        
        # Створюємо назву
        clean_name = file_path.stem.replace('_', ' ').replace('-', ' ').title()
        
        gallery_item = ProductGallery.objects.create(
            product=product,
            content_type=content_type,
            title_uk=clean_name,
            title_ru=clean_name,
            title_en=clean_name,
            alt_text=file_path.name,
            description=f"Файл {content_type.lower()} для {product.name_uk}",
            order=order,
            is_downloadable=True,
            file_size=self.get_file_size(file_path)
        )
        
        try:
            # Додаємо файл
            if content_type == 'IMAGE':
                with open(file_path, 'rb') as f:
                    gallery_item.image.save(file_path.name, File(f), save=False)
            else:
                with open(file_path, 'rb') as f:
                    gallery_item.file_3d.save(file_path.name, File(f), save=False)
                
                # Додаємо preview для 3D
                if preview_img and preview_img.exists():
                    with open(preview_img, 'rb') as f:
                        gallery_item.preview_image.save(f"preview_{file_path.name}.jpg", File(f), save=False)
            
            gallery_item.save()
            
            # Копіюємо файли для продакшену якщо потрібно
            if self.copy_files:
                self.copy_file_to_media(file_path, gallery_item, content_type)
            
            return True
            
        except Exception as e:
            self.stdout.write(f"❌ Помилка додавання {file_path.name}: {e}")
            gallery_item.delete()
            return False
    
    def copy_file_to_media(self, source_path, gallery_item, content_type):
        """Копіювати файл до media директорії для продакшену"""
        try:
            if content_type == 'IMAGE' and gallery_item.image:
                media_path = Path(settings.MEDIA_ROOT) / gallery_item.image.name
                media_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, media_path)
            elif gallery_item.file_3d:
                media_path = Path(settings.MEDIA_ROOT) / gallery_item.file_3d.name
                media_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, media_path)
        except Exception as e:
            self.stdout.write(f"⚠️  Помилка копіювання {source_path.name}: {e}")
    
    def get_file_size(self, file_path):
        """Отримати розмір файлу в зручному форматі"""
        size = file_path.stat().st_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
