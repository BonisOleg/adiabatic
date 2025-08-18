from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils.translation import get_language
from .models import Category, Product


def catalog_list(request):
    """Список всіх категорій та рекомендованих продуктів"""
    categories = Category.objects.filter(is_published=True).prefetch_related(
        'products__gallery', 'products__specifications'
    )
    
    # Рекомендовані продукти
    featured_products = Product.objects.filter(
        is_published=True, 
        is_featured=True
    ).select_related('category')[:6]
    
    # Всі продукти з пагінацією
    all_products = Product.objects.filter(is_published=True).select_related('category')
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
            'specifications', 'gallery', 'advantages', 'documents'
        ),
        slug=slug, 
        is_published=True
    )
    
    # Схожі продукти з тієї ж категорії
    related_products = Product.objects.filter(
        category=product.category,
        is_published=True
    ).exclude(id=product.id)[:4]
    
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
