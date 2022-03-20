from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

NUMBERS = [(1, '10_meters'), (5, '20_meters'), (10, '40_meters'), (25, '90_meters'), (50, '180_meters')]


class RegistrationUserForm(UserCreationForm):
    username = forms.CharField(max_length=30, label="Login:", widget=forms.TextInput(attrs={'class': "form-input"}))
    password1 = forms.CharField(label="Password:", widget=forms.PasswordInput(attrs={'class': "form-input"}))
    password2 = forms.CharField(label="Again Password:", widget=forms.PasswordInput(attrs={'class': "form-input"}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={'class': "form-input"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': "form-input"}))


class FileForm(forms.Form):
    file = forms.FileField(label="Добавить файл:")
    value = forms.TypedChoiceField(choices=NUMBERS, coerce=int,
                                   label="Сжатие")
