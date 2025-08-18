from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test_view, name='test'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('<slug:slug>/', views.page_detail, name='page_detail'),
]
