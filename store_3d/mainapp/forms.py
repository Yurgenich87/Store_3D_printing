from django import forms
from .models import User, Product, Order


class LoginForm(forms.Form):
    """Form for login"""
    email = forms.EmailField(label='Ваш email')
    password = forms.CharField(label='Ваш пароль', widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone', 'address']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Ваш ник'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Ваш пароль'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш еmail'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ваш телефон'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ваш адрес'}),
        }


class UserForm(forms.ModelForm):
    """ Form for creating new users"""
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone', 'address']
        labels = {
            'username': '',
            'password': '',
            'email': '',
            'phone': '',
            'address': '',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Ваш ник'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Ваш пароль'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш еmail'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ваш телефон'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ваш адрес'}),
        }


class ProductForm(forms.ModelForm):
    """Form for creating new products"""
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'image']
        labels = {
            'name': '',
            'description': '',
            'price': '',
            'quantity': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Товар'}),
            'description': forms.TextInput(attrs={'placeholder': 'Описание'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Цена'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Кол-во'}),
        }


class OrderForm(forms.ModelForm):
    """Form for creating new Orders"""
    class Meta:
        model = Order
        fields = ['user', 'product', 'quantity']

