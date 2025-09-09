from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import mimetypes
import os
from .models import Category, Product, ProductDocument


def catalog_list(request):
    """Список всіх категорій та рекомендованих продуктів"""
    categories = Category.objects.filter(is_published=True).prefetch_related(
        'products__gallery', 'products__specifications'
    )
    
    # Рекомендовані продукти
    featured_products = Product.objects.filter(
        is_published=True, 
        is_featured=True
    ).select_related('category').prefetch_related('gallery')[:6]
    
    # Всі продукти з пагінацією
    all_products = Product.objects.filter(is_published=True).select_related('category').prefetch_related('gallery')
    paginator = Paginator(all_products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'products': products,
        'page_title': 'Каталог продукції',
    }
    return render(request, 'catalog/catalog_list.html', context)


def category_detail(request, category_slug):
    """Детальна сторінка категорії з продуктами"""
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    
    products_list = Product.objects.filter(
        category=category, 
        is_published=True
    ).prefetch_related('gallery', 'specifications')
    
    # Пагінація
    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': products,
        'page_title': category.get_name(),
        'meta_description': category.get_description(),
    }
    return render(request, 'catalog/category_detail.html', context)


def product_detail(request, slug):
    """Детальна сторінка продукту"""
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related(
            'specifications', 'gallery', 'advantages'
        ),
        slug=slug, 
        is_published=True
    )
    
    # Схожі продукти з тієї ж категорії
    related_products = Product.objects.filter(
        category=product.category,
        is_published=True
    ).exclude(id=product.id).prefetch_related('gallery')[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
        'page_title': product.get_meta_title(),
        'meta_description': product.get_meta_description(),
        'specifications': product.specifications.all(),
        'gallery': product.gallery.all(),
        'advantages': product.advantages.all(),
        'documents': product.documents.filter(is_public=True),
    }
    return render(request, 'catalog/product_detail.html', context)


@require_http_methods(["GET"])
def download_document(request, doc_id):
    """Завантаження документу продукту"""
    try:
        document = get_object_or_404(ProductDocument, id=doc_id, is_public=True)
        
        # Збільшуємо лічильник доступу
        document.increment_access()
        
        # Відкриваємо файл
        if document.file and os.path.exists(document.file.path):
            with open(document.file.path, 'rb') as file:
                content = file.read()
            
            # Визначаємо MIME тип
            content_type, _ = mimetypes.guess_type(document.file.name)
            if not content_type:
                content_type = 'application/octet-stream'
            
            response = HttpResponse(content, content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(document.file.name)}"'
            
            return response
        else:
            raise Http404("Файл не знайдено")
            
    except Exception as e:
        raise Http404("Документ не знайдено")


def qr_document_view(request, qr_uuid):
    """Перегляд документу через QR код"""
    try:
        document = get_object_or_404(ProductDocument, qr_uuid=qr_uuid, is_public=True)
        
        # Збільшуємо лічильник доступу
        document.increment_access()
        
        context = {
            'document': document,
            'product': document.product,
            'page_title': f'Документ: {document.get_title()}',
        }
        
        return render(request, 'catalog/qr_document.html', context)
        
    except Exception as e:
        raise Http404("QR документ не знайдено")
