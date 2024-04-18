from django.db import models
from django.contrib.auth.models import User
from django.db.models import Manager


class Receipt(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=400)
    sequence_steps = models.TextField(max_length=500)
    time_to_cook = models.PositiveIntegerField()  # Время в минутах
    image = models.ImageField(upload_to='receipt_img/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category')
    objects = Manager()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150)
    objects = Manager()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = Manager()

    def __str__(self):
        return self.user.username