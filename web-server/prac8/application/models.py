import os

from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class User(models.Model):
    name = models.CharField(max_length=128)
    account = models.OneToOneField(AuthUser, null=True, on_delete=models.CASCADE)
    theme = models.IntegerField(default=0)
    language = models.CharField(max_length=2, default="ru")
    scale = models.FloatField(default=1.0)


class Services(models.Model):
    title = models.CharField(max_length=128)
    desc = models.TextField()
    price = models.FloatField()


class Entries(models.Model):
    customer_name = models.CharField(max_length=128)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    amount = models.IntegerField()
    comment = models.TextField(null=True, blank=True)


class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')


@receiver(pre_delete, sender=ImageModel)
def delete_image_on_model_delete(sender, instance, **kwargs):
    if instance.image:
        # Получаем путь к файлу изображения
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
