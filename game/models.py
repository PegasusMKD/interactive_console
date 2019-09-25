from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class GameUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=30,default='')


class Option(models.Model):
    title = models.CharField(max_length=160)
    user = models.ForeignKey(GameUser,on_delete=models.CASCADE, related_name="options")


class Chapter(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    option = models.ForeignKey(Option,on_delete=models.CASCADE, related_name="chapters")
    solved = models.BooleanField(default=False)
    

class Exercises(models.Model):
    chapter = models.OneToOneField(Chapter,on_delete=models.SET_NULL,null=True,related_name="exercise")
    title = models.CharField(max_length=175)
    description = models.CharField(max_length=255)
    sample_code = models.TextField()
    answer = models.CharField(max_length=255)
    reward = models.CharField(max_length=255)
    solved = models.BooleanField(default=False)

    def __str__(self):
        return f"Exercise: {self.title} - Descrition: {self.description} - Answer: {self.answer}"

