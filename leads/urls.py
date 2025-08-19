from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    # AJAX endpoints
    path('submit/', views.submit_lead, name='submit'),
    path('quick-quote/', views.quick_quote, name='quick_quote'),
    path('contact/', views.contact, name='contact'),
    
    # Success/Thank you pages
    path('thank-you/', views.thank_you, name='thank_you'),
    path('thank-you/<uuid:lead_uuid>/', views.thank_you_detail, name='thank_you_detail'),
]
