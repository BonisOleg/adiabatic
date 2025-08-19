from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('products/', views.products, name='products'),
    path('<slug:slug>/', views.page_detail, name='page_detail'),
]
