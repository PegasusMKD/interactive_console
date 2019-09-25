import json
import urllib.parse

from django.shortcuts import HttpResponse,render_to_response
from .main_funcs import *
from .models import *

def got_correct(request):
    return HttpResponse(json.dumps(correct(request)))

# Create your views here.
def get_options(request):
    return HttpResponse(json.dumps(retrieve_options(request)))
def get_chapters(request):
    return HttpResponse(json.dumps(retrieve_chapters(request)))

def get_chapter(request):
    return HttpResponse(json.dumps(retrieve_chapter(request)))


def display_exercise(request,answer):
    print(answer)
    exercise = displaying_exercise(answer)
    context = dict()
    if request.method == "POST":
        data = urllib.parse.parse_qsl(request.body.decode('utf-8'))
        if isinstance(data,str):
            data = convert_string_to_dictionary(data)
        elif isinstance(data,list):
            data = dict(data)
        print(data)
        tmp_exercise = Exercises.objects.get(title=data['exercise'])

        if data['answer'] == tmp_exercise.answer:
            tmp_exercise.solved = True
            tmp_exercise.save(update_fields=['solved'])
            context['message'] = tmp_exercise.reward
        else:
            context['message'] = "Wrong Answer!"

        context['exercise'] = tmp_exercise

    elif request.method == "GET":
        context = {
            'exercise' : exercise,
            'message' : False,
            'answer' : answer
            }

    return render_to_response('game/index.html', context)

