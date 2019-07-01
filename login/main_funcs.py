from .models import *
import json
import string
import random

"""
Extras
"""

def new_hash(size=26, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


"""
Main functions
"""

def try_login(request):
    req = json.loads(request.body)
    try:
        user = User.objects.get(username=req['username'])
    except:
        return json.dumps({
            'response' : random.choice(Failed.objects.filter(type='username')).text   #'Утнат user, sowwie >,<'
        })

    if user.password == req['password']:

        if user.token == '':
            user.token = new_hash()
            user.save(update_fields=['token'])
            return json.dumps({
                'token' : user.token,
                'response' : 'Wowie, u is a hackew i see UwU!\n\n' + random.choice(user.intros.all()).text
            })
        else:
            user.token = new_hash()
            user.save(update_fields=['token'])
            return json.dumps({
                'token': user.token,
                'response': random.choice(user.intros.all()).text
            })

    else:
        return json.dumps({
            'response': random.choice(user.failed.filter(type='password')).text
        })


def looking_for(request):
    req = json.loads(request.body)
    user = User.objects.get(token=req['token'])
    try:
        user_looking_for = User.objects.get(name=req['user_looking_for'])
        user_looking_for.looked_up += 1
        user_looking_for.recognized = new_hash()
        user_looking_for.save(['looked_up','recognized'])
    except:
        return json.dumps({
            'response' : [random.choice(user.failed.filter(type='not_found')).text,False]
        })

    return json.dumps({
        'response' : [random.choice(user.responses).text,user_looking_for.recognized,True]
    })

def douchy_response(request):
    req = json.loads(request.body)
    user = User.objects.get(token=str(req['token']))
    return {
        'response' : random.choice(user.failed.filter(type='smartass')).text
    }