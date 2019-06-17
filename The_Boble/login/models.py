from django.db import models

from django.contrib.postgres.fields import ArrayField


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    looked_up = models.IntegerField()
    recognized = models.CharField(max_length=30)
    token = models.CharField(max_length=30,default='')
    friends = ArrayField(
        models.CharField(max_length=75),
        default=list,
        null=True,
        blank=True
    )

class Intro(models.Model):
    text = models.CharField(max_length=150)
    user = models.ManyToManyField(User, related_name='intros')

class Failed(models.Model):
    text = models.CharField(max_length=150)
    type = models.CharField(max_length=150)
    user = models.ManyToManyField(User, related_name='failed')

class Responses(models.Model):
    text = models.CharField(max_length=150)
    user = models.ManyToManyField(User, related_name='responses')
