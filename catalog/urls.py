from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog_list, name='catalog_list'),
    path('category/<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    # Документи та QR коди
    path('document/<int:doc_id>/download/', views.download_document, name='download_document'),
    path('qr/<uuid:qr_uuid>/', views.qr_document_view, name='qr_document_view'),
]
