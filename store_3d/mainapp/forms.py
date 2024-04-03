from django import forms
from .models import User, Product, Order


class LoginForm(forms.Form):
    """Form for login"""
    email = forms.EmailField(label='Ваш email')
    password = forms.CharField(label='Ваш пароль', widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль', required=False)
    password_confirmation = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'patronymic_name', 'phone', 'street', 'city',
                  'region', 'postal_code']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Пароль и подтверждение пароля не совпадают.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            initial_data = {
                'username': self.instance.username,
                'email': self.instance.email,
                'first_name': self.instance.first_name,
                'last_name': self.instance.last_name,
                'patronymic_name': self.instance.patronymic_name,
                'phone': self.instance.phone,
                'street': self.instance.street,
                'city': self.instance.city,
                'region': self.instance.region,
                'postal_code': self.instance.postal_code
            }
            self.initial = initial_data

    def clean(self):
        """Clean method to validate password confirmation"""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class UserForm(forms.ModelForm):
    """ Form for creating new users"""
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone']
        labels = {
            'username': '',
            'password': '',
            'email': '',
            'phone': '',
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
        fields = ['name', 'description', 'price', 'quantity', 'category_id']
        labels = {
            'name': '',
            'price': '',
            'quantity': '',
            'description': '',
            'category_id': ''

        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Товар'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Цена'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Кол-во'}),
            'description': forms.TextInput(attrs={'placeholder': 'Описание'}),
            'category_id': forms.TextInput(attrs={'placeholder': 'Категория'}),
        }


class ImageForm(forms.Form):
    """Form for uploading images"""
    image = forms.ImageField()


class OrderForm(forms.ModelForm):
    """Form for creating new Orders"""
    class Meta:
        model = Order
        fields = ['user', 'product']
