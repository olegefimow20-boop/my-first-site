from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Model
from django.utils import timezone


class User(AbstractUser):
    fio = models.CharField(max_length=100)
    phone = models.CharField(max_length=11, unique=True, null=True)
    email = models.EmailField(unique=True)
    regdate = models.DateField(default=timezone.now())
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Добавляем поле для аватара

class Statement(Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state=models.CharField(max_length=150)
    description=models.CharField(max_length=500)
    status=models.CharField(max_length=20, default='На рассмотрении')
    date = models.DateField(default=timezone.now())

class News(Model):
    date = models.DateField(default=timezone.now)
    text = models.CharField(max_length=150)
    image = models.ImageField(upload_to='images', blank=True)
    time = models.TimeField(default=timezone.now)
    

class Services(Model):
    serviceimg = models.ImageField(upload_to='images', blank=True)
    title = models.CharField(max_length=150)
    servicedescription = models.CharField(max_length=150)