from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User as AuthUser
from .models import *


LANGUAGE_LABELS = {
    'en': {
        'username': 'Username',
        'password': 'Password',
        'name': 'Name',
    },
    'ru': {
        'username': 'Имя пользователя',
        'password': 'Пароль',
        'name': 'Имя',
    },
}


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = AuthUser
        fields = ('username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', max_length=254)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", )

    name = forms.CharField(label="Имя пользователя", max_length=254)

    def __init__(self, *args, lang, **kwargs):
        super().__init__(*args, **kwargs)
        labels = LANGUAGE_LABELS.get(lang, LANGUAGE_LABELS['ru'])  # Получаем метки для текущего языка
        self.fields['name'].label = labels['username']


class CreateServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ("title", "desc", "price")