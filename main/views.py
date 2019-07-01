from django.shortcuts import HttpResponse

from .main_funcs import *
# Create your views here.


def offer_recipes(request):
    return HttpResponse(offering_recipes(request))

def find_recipes(request):
    return HttpResponse(find_recipe(request))

def find_levels(request):
    return HttpResponse(found_levels(request))