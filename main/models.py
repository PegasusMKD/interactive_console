from django.db import models

from login.models import User
from django.contrib.postgres.fields import ArrayField

from postgres_copy import CopyManager
# Create your models here.

class Level(models.Model):
    objects = CopyManager()
    name = models.CharField(max_length=75)  #Dodadi easter egg (woops, broke the damn server cause it was worse than hell...)

class Category(models.Model):
    objects = CopyManager()
    name = models.CharField(max_length=100)

class Ingredient(models.Model):
    objects = CopyManager()
    name = models.CharField(max_length=175)
    category = models.ManyToManyField(Category,related_name='ingredients')

class Recipe(models.Model):
    objects = CopyManager()
    user = models.ManyToManyField(User,related_name='user_recipes')
    level = models.ForeignKey(Level, on_delete=models.SET_NULL,related_name='lvl_recipes',null=True)
    level_of_torture = models.IntegerField()
    index_of_recipe = models.IntegerField()
    name = models.CharField(max_length=150)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    ingredient_ammount = ArrayField(
        models.IntegerField(),
        default=list,
        blank=True,
        null=True
    )
    instructions = models.TextField()

    """
    Example 1:
    
    
    """