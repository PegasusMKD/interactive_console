import requests
import json
from itertools import islice
import time

import msvcrt as m

"""
Extras
"""
def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)

def wait():
    m.getch()

def payload(url,path,payload={}):
     request = requests.post('https://theboble.herokuapp.com/{}/{}/'.format(url,path),headers={'Content-Type' : 'application/json'},data=json.dumps(payload))
     #print(request.content)
     return json.loads(request.content)

#def payload(url,path,payload={}):
#    request = requests.post('http://127.0.0.1:8000/{}/{}/'.format(url,path),headers={'Content-Type' : 'application/json'},data=json.dumps(payload))
#    return json.loads(request.content)

"""
Main functions
"""

def login(counter=0):
    username = input('Username:')
    password = input('Password:')
    data = {
        'username' : username,
        'password' : password
    }
    response = payload('login','login',data)
    
    if 'token' in response.keys():
        print(response['response'])
        print()
        return [True,response['token'],response['type']]

    elif counter == 0:
        print('Huh, did he forget to give you the username and password?')
        print('Aw shucks, but hey! You two are good friends, SURELY you can think of something')
        print('His mind is quite simple, think of something related to the two of you...')
        return login(counter+1)

    else:
        print(response['response'])
        return login(counter+1)



def looking_up(look_up,token):
    if look_up.lower() == 'yes':
        who_to_look_for = input('Please enter their name:')
        data = {
            'user_looking_for' : who_to_look_for,
            'token' : token
        }
        response = payload('login','looking_for',data)

        if response['response'][-1]:
            print(response['response'][0])
            return response['response'][1]
        else:
            print(response['response'][0])
            print()
            print("Want to try someone else?(yes/no)")
            looking_up(input(),token)

        return True

    elif look_up.lower() == 'no':
        print('Okie, your choice!')
        return True

    else:
        response = payload('login','douche',{'token' : token})
        print(response['response'])
        looking_up(input('Now, be kind enough to give a proper answer :)\n(yes/no)'), token)
        return True

def offered_recipes(token,level,recognized=""):
    if recognized == "":
        data = {
            'token' : token,
            'level' : level,
        }
    else:
        data = {
            'recognized' : recognized,
            'token': token,
            'level': level,
        }

    return payload('main','offer_recipes', data)


def get_level(token,last_levels = []):
    print("What level would you like?")
    counter = 1
    if last_levels == []:
        levels = payload('main','find_levels', {'token': token})['levels']
    else: 
        levels = last_levels

    for x in levels:
        print(str(counter) + '. ' + x)
        counter += 1

    level = input('Enter the level you\'d want:')
    if str.isdigit(level):
        if int(level) > len(levels):
            print("Alo shmekeri, ona nije moja!")
            return get_level(token,levels)
        else:
            return levels[int(level)-1]

    elif level in levels:
        return level
    else:
        return False


def get_recipe(recipe,token):
    data = {
        'token' : token,
        'recipe' : recipe
    }
    return payload('main','find_recipe',data)


def parser(instructions):
    new_instructions = list(instructions)
    tmp_value = [instructions.split(" ").index(i) for i in instructions.split(" ") if i == "\n\n"][0]
    value = len(''.join(instructions.split(" ")[:tmp_value]))
    #print(''.join(new_instructions[:value]))
    new_instructions = new_instructions[value:]
    sum = 0
    try:
        length = len(new_instructions)
        if length % 75 != 0:
            length -= length % 75
        for x in range(75,length+75,75):
            sum += 75
            if new_instructions[x-1] == ' ' or new_instructions[x-1] == '.':
                print(''.join(new_instructions[x-75:x]))
            else:
                new_instructions.insert(x-1,'-')
                print(''.join(new_instructions[x-75:x]))
            wait()

        print(''.join(new_instructions[length:-1]))
    except:
        return True
    return True


def print_recipe(recipe):
    print("[Level: {}]".format(recipe['level']))
    print("\\\\\\\\Torture level: {}/9000\\\\\\\\".format(recipe['level_of_torture']))
    print("Recipe {}: {}".format(recipe['index_of_recipe'],recipe['recipe_name']))
    print("[Ingredients]")
    parser(recipe['instructions'])
    return True


def actual_main(token):
    print('Would you like to take a look at someone specific?(yes/no)')
    look_up = input()
    looked = looking_up(look_up, token)
    print()
    recipes = offer_levels(looked, token)
    print()
    #print(recipes)
    print(recipes['welcome_response'])
    counter = 1
    for x in recipes['response']:
        print(str(counter) + '. ' + x)
        counter += 1

    recipe = recipes_loop(recipes, token)
    print()

    finished = print_recipe(recipe)
    print()

    if finished:
        another = input("Want to go again? (yes/no)\n")
        if another.lower() == 'yes':
            actual_main(token)
        else:
            print("Thank you for coming, hope we see you back soon!")
            time.sleep(30)


def recipes_loop(recipes, token):
    recipe_name = input("What shall we have:")
    #print(recipe_name in recipes['response'])
    if str.isdigit(recipe_name):
        if int(recipe_name) > len(recipes['response']):
            print("Nice tryy ~(0.0)~")
            recipe = recipes_loop(recipes,token)

        else:
            recipe = get_recipe(recipes['response'][int(recipe_name) - 1], token)

    elif recipe_name in recipes['response']:
        recipe = get_recipe(recipe_name, token)
    else:
        print("Not a shmart move, i must say...")
        recipe = recipes_loop(recipes,token)
    return recipe


def offer_levels(looked, token):
    if isinstance(looked, str):

        level = get_level(token)
        if level is not False:
            recipes = offered_recipes(token, level, looked)
            if not isinstance(recipes['response'],list):
                print(recipes['response'])
                return offer_levels(looked,token)
        else:
            return offer_levels(looked,token)

    else:
        level = get_level(token)
        if level is not False:
            recipes = offered_recipes(token, level)
            if not isinstance(recipes['response'],list):
                print(recipes['response'])
                return offer_levels(looked,token)
        else:
            return offer_levels(looked,token)

    return recipes


def main():
    print('Why hello there, i see you\'re a close friend of Pazzio\'s!')
    details = login()
    token = details[1]
    type = details[2]
    if details[0]:
        if type == "bob":
            actual_main(token)
        elif type == "game":
            pass

main()

def game_main(token):
    recipes = offer_levels(looked, token)
    print()
    #print(recipes)
    print(recipes['welcome_response'])
    counter = 1
    for x in recipes['response']:
        print(str(counter) + '. ' + x)
        counter += 1

    recipe = recipes_loop(recipes, token)
    print()

    finished = print_recipe(recipe)
    print()

    if finished:
        another = input("Want to go again? (yes/no)\n")
        if another.lower() == 'yes':
            actual_main(token)
        else:
            print("Thank you for coming, hope we see you back soon!")
            time.sleep(30)