
from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
    path('offer_recipes/',views.offer_recipes, name="offer_recipes"),
    path('find_recipe/',views.find_recipes, name="find_recipes"),

]
