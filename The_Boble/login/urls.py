
from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
    path('login/',views.login, name="login"),
    path('looking_for/',views.looking_for,name='looking_for'),
    path('douche/',views.douche_response,name='douche')

]
