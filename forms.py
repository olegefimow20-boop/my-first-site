from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User,Statement,News, Services


class UserRegistrationForm(UserCreationForm):
    avatar = forms.ImageField(required=False, label='Аватар')  # Добавляем поле для аватара
    
    class Meta:
        model = User
        fields = ['username', 'fio', 'phone', 'email', 'password1', 'password2', 'avatar']
        labels = {
            'fio': 'Введите ФИО:',
            'phone': 'Введите номер телефона:',
            'email': 'Введите почту:',
        }

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']



class CreateStatement(forms.ModelForm):
    class Meta:
        model = Statement
        fields = ['state', 'description']
        labels = {
            'state': 'Введите название услуги:',
            'description': 'Опишите причину заявления:'
        }

class AddNews(forms.ModelForm):
    class Meta:
        model = News
        fields = ['text','image']
        labels = {
            'text': 'Введите новостной заголовок:',
            'image': 'Добавьте изображение:'
        }

class CreateService(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['title','serviceimg','servicedescription']
        labels = {
            'title': 'Введите заголовок:',
            'serviceimg': 'Добавьте изображение:',
            'servicedescription': 'Добавьте описание услуги:'
        }