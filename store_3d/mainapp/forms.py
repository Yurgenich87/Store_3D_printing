from django import forms
from .models import User, Product, Order

from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    email = forms.EmailField(label='Ваш email')
    password = forms.CharField(label='Ваш пароль', widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
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


class ProductForm(forms.Form):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity']


class OrderForm(forms.Form):
    class Meta:
        model = Order
        fields = ['user', 'product', 'price_sum']
