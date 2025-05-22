from django.forms import ModelForm
from .models import Review, ProductImage, User,Product
from django.db.models import Max
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_phone(value):
    if not all(c in '+0123456789' for c in value):
        raise ValidationError(
            _('Номер телефона может содержать только цифры и символ "+".')
        )

class GuestOrderForm(forms.Form):    
    first_name = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
        label='Имя'
    )
    last_name = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
        label='Фамилия'
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
        label='Номер телефона',
        validators=[validate_phone] 
    )
    email = forms.EmailField(
        required=False, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='Email (опционально)'
    )

class MyUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Пароль', 
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Подтверждение пароля', 
        widget=forms.PasswordInput
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class MyUserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']

    phone_number = forms.CharField(
        max_length=20,
        required=False,
        validators=[validate_phone]
    )


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = '__all__'


class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','amount','year']
        labels = {
            'name': 'Название',
            'price': 'Цена',
            'amount': 'Количество',
            'year': 'Год выхода на рынок',
        }
