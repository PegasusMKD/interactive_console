from .models import *
from game.models import GameUser
import json
import string
import random
import os
import traceback

"""
Extras
"""

def new_hash(size=26, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def back_up_from_server():
    folder = "back/testing/"
    try:
        os.makedirs(folder)
    except:
        pass

    User.objects.to_csv(folder + "user.csv",encoding='utf-8')
    Intro.objects.to_csv(folder + "intro.csv",encoding='utf-8')
    Failed.objects.to_csv(folder + "failed.csv",encoding='utf-8')
    Responses.objects.to_csv(folder + "responses.csv",encoding='utf-8')


"""
Main functions
"""

def try_login(request):
    req = json.loads(request.body)
    try:
        user = User.objects.get(username=req['username'])
    except:
        try:
            user = GameUser.objects.get(username=req['username'])
        except:
            return json.dumps({
            'response' : random.choice(Failed.objects.filter(type='username')).text   #'Утнат user, sowwie >,<'
            })

    failed_passwords = user.game_failed.filter(type='password') if type(user) is GameUser else user.failed.filter(type='password')

    if user.password == req['password']:
        intros = user.game_intros.all() if type(user) is GameUser else user.intros.all()
        if user.token == '':
            user.token = new_hash()
            user.save(update_fields=['token'])
            return json.dumps({
                'token' : user.token,
                'type' : 'game' if type(user) is GameUser else 'bob',
                'response' : 'Wowie, u is a hackew i see UwU!\n\n' + random.choice(intros).text
            })
        else:
            user.token = new_hash()
            user.save(update_fields=['token'])
            return json.dumps({
                'token' : user.token,
                'type' : 'game' if type(user) is GameUser else 'bob',
                'response' : random.choice(intros).text
            })

    else:
        return json.dumps({
            'response': random.choice(failed_passwords).text
        })


def looking_for(request):
    try:
        req = json.loads(request.body)
        user = User.objects.get(token=req['token'])
        try:
            user_looking_for = User.objects.get(name=req['user_looking_for'])
            user_looking_for.looked_up += 1
            user_looking_for.recognized = new_hash()
            user_looking_for.save(update_fields=['looked_up','recognized'])
        except:
            return json.dumps({
                'response' : [random.choice(user.failed.filter(type='not_found')).text,False]
            })

        return json.dumps({
            'response' : [random.choice(user.responses.all()).text,user_looking_for.recognized,True]
        })
    except:
        print(traceback.format_exc())


def douchy_response(request):
    req = json.loads(request.body)
    try:
        user = User.objects.get(token=str(req['token']))
    except:
        user = GameUser.objects.get(token=str(req['token']))

    smartass_fails = user.game_failed.filter(type='smartass') if user is GameUser else user.failed.filter(type='smartass')

    return {
        'response' : random.choice(smartass_fails).text
    }