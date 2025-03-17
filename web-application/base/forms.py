from django.forms import ModelForm
from .models import Mouse, Keyboard, Headphones, Review, SharedID, ProductImage, User,Product
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
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'Email': 'Email',
        }

class MyUserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone_number': 'Номер телефона',
        }

    phone_number = forms.CharField(
        max_length=20,
        required=False,
        validators=[validate_phone]
    )


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone_number': 'Номер телефона',
        }


class SharedID(ModelForm):
    class Meta:
        model = SharedID
        fields = '__all__'

class MouseForm(ModelForm):
    class Meta:
        model = Mouse
        fields = ['name', 'price', 'amount', 'date', 'type', 'wireless','sensor_type', 'sensor_model','max_sens_res','max_pooling_rate','body_material', 'backlight']
        labels = {
            'name': 'Название',
            'price': 'Цена',
            'amount': 'Количество',
            'date': 'Дата выхода на рынок',
            'type': 'Тип',
            'wireless': 'Беспроводная',
            'sensor_type': 'Тип сенсора',
            'sensor_model': 'Модель сенсора',
            'max_sens_res': 'Максимальное разрешение сенсора',
            'max_pooling_rate': 'Максимальная частота опроса',
            'body_material': 'Материал корпуса',
            'backlight': 'Подсветка',
        }

class KeyboardForm(ModelForm):
    class Meta:
        model = Keyboard
        fields = ['name', 'price', 'amount', 'date', 'type', 'switch_type','switch_name', 'color','сyrillic','wireless','cable_sleeving']
        
        labels = {
            'name': 'Название',
            'price': 'Цена',
            'amount': 'Количество',
            'date': 'Дата выхода на рынок',
            'type': 'Тип',
            'switch_type': 'Тип переключателей',
            'switch_name': 'Название переключателей',
            'color': 'Цвет',
            'сyrillic': 'Кириллица',
            'wireless': 'Беспроводная',
            'cable_sleeving': 'Оплётка кабеля',
        }

class HeadphonesForm(ModelForm):
    class Meta:
        model = Headphones
        fields = ['name', 'price', 'amount', 'date', 'type', 'wireless','ruggedness', 'body_material','headphone_color','cable_color','earpad_material']

        labels = {
            'name': 'Название',
            'price': 'Цена',
            'amount': 'Количество',
            'date': 'Дата выхода на рынок',
            'type': 'Тип',
            'wireless': 'Беспроводные',
            'ruggedness': 'Пыле-, влаго-защита',
            'body_material': 'Материал корпуса',
            'headphone_color': 'Цвет наушников',
            'cable_color': 'Цвет кабеля',
            'earpad_material': 'Материал амбушюр',
        }

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