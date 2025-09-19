from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from .models import Lead


class LeadForm(forms.ModelForm):
    """Базова форма заявки"""
    
    # Honeypot поле для захисту від ботів
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label="Website (leave blank)"
    )
    
    # Перевизначаємо поле телефону з кращою валідацією
    phone = forms.CharField(
        label=_('Телефон'),
        max_length=17,
        validators=[
            RegexValidator(
                regex=r'^\+?[1-9]\d{1,14}$',
                message=_('Введіть коректний номер телефону (наприклад: +380501234567)')
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': '+380501234567',
            'class': 'form__input',
            'pattern': r'^\+?[1-9]\d{1,14}$',
            'title': _('Формат: +380501234567')
        })
    )
    
    class Meta:
        model = Lead
        fields = [
            'name', 'email', 'phone', 'company', 'position',
            'inquiry_type', 'product_name', 'subject', 'message',
            'budget_range', 'project_timeline',
            'consent_gdpr', 'consent_marketing'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': _('Ваше ім\'я'),
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form__input',
                'placeholder': _('Ваш email'),
                'required': True,
            }),
            'company': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': _('Назва компанії (опційно)'),
            }),
            'position': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': _('Ваша посада'),
            }),
            'inquiry_type': forms.Select(attrs={
                'class': 'form__input',
            }),
            'product_name': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': _('Тип обладнання або продукт'),
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': _('Тема запиту'),
            }),
            'message': forms.Textarea(attrs={
                'class': 'form__textarea',
                'placeholder': _('Опишіть ваш запит детальніше...'),
                'rows': 4,
                'required': True,
            }),
            'budget_range': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': _('Наприклад: $10,000 - $50,000'),
            }),
            'project_timeline': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': _('Наприклад: протягом 3 місяців'),
            }),
            'consent_gdpr': forms.CheckboxInput(attrs={
                'class': 'form__checkbox-input',
                'required': True,
            }),
            'consent_marketing': forms.CheckboxInput(attrs={
                'class': 'form__checkbox-input',
            }),
        }
        
        labels = {
            'name': _('Ім\'я *'),
            'email': _('Email *'),
            'phone': _('Телефон *'),
            'company': _('Компанія'),
            'position': _('Посада'),
            'inquiry_type': _('Тип запиту'),
            'product_name': _('Продукт'),
            'subject': _('Тема'),
            'message': _('Повідомлення *'),
            'budget_range': _('Бюджет проекту'),
            'project_timeline': _('Терміни реалізації'),
            'consent_gdpr': _('Я погоджуюся на обробку персональних даних *'),
            'consent_marketing': _('Я погоджуюся на отримання маркетингових повідомлень'),
        }
    
    def __init__(self, *args, **kwargs):
        # Витягуємо додаткові параметри
        self.product_name_initial = kwargs.pop('product_name', None)
        super().__init__(*args, **kwargs)
        
        # Якщо передано назву продукту, встановлюємо її як початкове значення
        if self.product_name_initial:
            self.fields['product_name'].initial = self.product_name_initial
            # Встановлюємо тему за замовчуванням
            if not self.initial.get('subject'):
                self.fields['subject'].initial = f"{_('Запит щодо')} {self.product_name_initial}"
    
    def clean_website(self):
        """Honeypot валідація - поле має бути пустим"""
        website = self.cleaned_data.get('website')
        if website:
            raise forms.ValidationError(_('Спам детектовано.'))
        return website
    
    def clean_phone(self):
        """Додаткова валідація телефону"""
        phone = self.cleaned_data.get('phone', '').strip()
        
        # Видаляємо всі пробіли та дефіси
        phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # Перевіряємо базовий формат
        if not phone:
            raise forms.ValidationError(_('Телефон є обов\'язковим полем.'))
        
        # Додаємо + якщо немає
        if not phone.startswith('+') and phone.startswith('380'):
            phone = '+' + phone
        elif not phone.startswith('+') and not phone.startswith('380'):
            phone = '+380' + phone
        
        return phone
    
    def clean(self):
        """Загальна валідація форми"""
        cleaned_data = super().clean()
        
        # Перевіряємо згоду на GDPR
        consent_gdpr = cleaned_data.get('consent_gdpr')
        if not consent_gdpr:
            raise forms.ValidationError(_('Необхідно надати згоду на обробку персональних даних.'))
        
        return cleaned_data


class QuickQuoteForm(forms.ModelForm):
    """Швидка форма запиту ціни (мінімальні поля)"""
    
    # Honeypot
    website = forms.CharField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = Lead
        fields = ['name', 'phone', 'email', 'product_name', 'message', 'consent_gdpr']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': _('Ваше ім\'я'),
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': '+380501234567',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form__input',
                'placeholder': _('Ваш email'),
                'required': True,
            }),
            'product_name': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': _('Тип обладнання'),
            }),
            'message': forms.Textarea(attrs={
                'class': 'form__textarea',
                'placeholder': _('Додаткові коментарі (опційно)'),
                'rows': 3,
            }),
            'consent_gdpr': forms.CheckboxInput(attrs={
                'class': 'form__checkbox-input',
                'required': True,
            }),
        }
        
        labels = {
            'name': _('Ім\'я *'),
            'phone': _('Телефон *'),
            'email': _('Email *'),
            'message': _('Коментарі'),
            'consent_gdpr': _('Згода на обробку даних *'),
        }
    
    def __init__(self, *args, **kwargs):
        self.product_name_value = kwargs.pop('product_name', None)
        super().__init__(*args, **kwargs)
        
        # Встановлюємо назву продукту
        if self.product_name_value:
            self.fields['product_name'].initial = self.product_name_value
            # Встановлюємо inquiry_type
            self.inquiry_type = 'price_request'
    
    def clean_website(self):
        website = self.cleaned_data.get('website')
        if website:
            raise forms.ValidationError(_('Спам детектовано.'))
        return website
    
    def save(self, commit=True):
        lead = super().save(commit=False)
        lead.inquiry_type = 'price_request'
        lead.subject = f"{_('Швидкий запит ціни')} - {lead.product_name if lead.product_name else _('Загальний запит')}"
        
        if commit:
            lead.save()
        return lead


class ContactForm(forms.ModelForm):
    """Форма контактів (загальна)"""
    
    # Honeypot
    website = forms.CharField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'company', 'inquiry_type', 'subject', 'message', 'consent_gdpr']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': _('Ваше ім\'я'),
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form__input',
                'placeholder': _('Ваш email'),
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': '+380501234567',
            }),
            'company': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': _('Назва компанії'),
            }),
            'inquiry_type': forms.Select(attrs={
                'class': 'form__input',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': _('Тема повідомлення'),
            }),
            'message': forms.Textarea(attrs={
                'class': 'form__textarea',
                'placeholder': _('Ваше повідомлення...'),
                'rows': 5,
            }),
            'consent_gdpr': forms.CheckboxInput(attrs={
                'class': 'form__checkbox-input',
                'required': True,
            }),
        }
    
    def clean_website(self):
        website = self.cleaned_data.get('website')
        if website:
            raise forms.ValidationError(_('Спам детектовано.'))
        return website


class LeadStatusForm(forms.ModelForm):
    """Форма для оновлення статусу заявки (для адмінки)"""
    
    class Meta:
        model = Lead
        fields = ['status', 'internal_notes', 'contacted_at']
        
        widgets = {
            'status': forms.Select(attrs={'class': 'form__input'}),
            'internal_notes': forms.Textarea(attrs={
                'class': 'form__textarea',
                'rows': 3,
                'placeholder': _('Внутрішні примітки...')
            }),
            'contacted_at': forms.DateTimeInput(attrs={
                'class': 'form__input',
                'type': 'datetime-local'
            }),
        }
