from .models import *
import json
import string
import random
import os
import traceback

"""
Game Type of Display

Page #1
    1. Rules of the game
    2. Puzzles ( Starter Point )

Page #2

    1. Name 1
    If Name 1 fully read:
    2. Name 2
    .
    .
    .

    Name Pages Template
        Chapter 1: Name 1
        
        Lore
        .
        .
        .



Next Level of the game:
    Fix up some Python code
    Couple of partially finished code, with a couple of missing pieces
    Few exercises
    Answers are an encoded URL

    Example: 
        a = 
        a.append(1)

        for idx, <missing> in smtn:
            print(idx + str(<missing>))


Next Level of the game:
    For each code exercise done, you get a reward

    Reward Box includes one of the following:
     - Meme
     - Some heartfelt text
     - Cute gif
     - Picture of someone ( idfk )





"""


"""
Main Functions
"""

def retrieve_options(request):
    req = json.loads(request.body)
    user = GameUser.objects.get(token = req['token'])
    response = {
        'options' : [x.title for x in user.options.all()],
        }
    return response



def retrieve_chapters(request):
    req = json.loads(request.body)
    user = GameUser.objects.get(token = req['token'])
    option = user.options.get(title=req['option'])
    response = {
        'welcome_response' : random.choice(user.game_intros.all()).text,
        'response' : [x.title for x in option.chapters.all()],
        }
    return response


def retrieve_chapter(request):
    req = json.loads(request.body)
    user = GameUser.objects.get(token = req['token'])
    option = user.options.get(title=req['option'])
    chapters = [x.title for x in option.chapters.all()]

    if req['chapter'] in chapters:
        chapter = option.chapters.get(title = req['chapter'])

        response = {
            'title' : chapter.title,
            'text' : chapter.text,
            'question' : chapter.question,
            'answer' : chapter.answer,
            }

    else:
        return False

    return response


def correct(request):
    req = json.loads(request.body)
    user = GameUser.objects.get(token=req['token'])
    response = {"response" : random.choice(user.game_responses.filter(type="correct")).text}
    return response



def displaying_exercise(answer):
    try:
        chapter = Chapter.objects.get(answer=answer)
        if not chapter.solved:
            chapter.solved = True
            chapter.save(update_fields=['solved'])

    except:
        return False

    return chapter.exercise


def convert_string_to_dictionary(string):
    dictionary = dict()
    words = string.split("=")
    for idx,word in enumerate(words[::2]):
        dictionary[word] = words[idx+1]

    return dictionary