from django.shortcuts import HttpResponse
from .main_funcs import *


# Create your views here.


def login(request):
    return HttpResponse(login(request))

def looking_up(request):
    return HttpResponse(looking_for(request))

def douche_response(request):
    return HttpResponse(json.loads(douche_response(request)))