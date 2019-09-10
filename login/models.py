from django.db import models

from django.contrib.postgres.fields import ArrayField

from postgres_copy import CopyManager

# Create your models here.

class User(models.Model):
    objects = CopyManager()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    looked_up = models.IntegerField(null=True)
    recognized = models.CharField(max_length=30,default='')
    token = models.CharField(max_length=30,default='')
    friends = ArrayField(
        models.CharField(max_length=75),
        default=list,
        null=True,
        blank=True
    )

class Intro(models.Model):
    objects = CopyManager()
    text = models.CharField(max_length=150)
    user = models.ManyToManyField(User, related_name='intros')

class Failed(models.Model):
    objects = CopyManager()
    text = models.CharField(max_length=150)
    type = models.CharField(max_length=150)
    user = models.ManyToManyField(User, related_name='failed')

class Responses(models.Model):
    objects = CopyManager()
    text = models.CharField(max_length=150)
    user = models.ManyToManyField(User, related_name='responses')
