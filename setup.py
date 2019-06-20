import requests
import json
from itertools import islice
import time


"""
Extras
"""
def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)


# def payload(url,path,payload={}):
    # request = requests.post('http://127.0.0.1:8000/{}/{}/'.format(url,path),header={'Content-Type' : 'application/json'},data=json.loads(payload))
    # return json.loads(request.content)

def payload(url,path,payload={}):
    request = requests.post('https://theboble.herokuapp.com/{}/{}/'.format(url,path),headers={'Content-Type' : 'application/json'},data=json.dumps(payload))
    print(request.content)
    return json.loads(request.content)

"""
Main functions
"""
def login():
    username = input('Username:')
    password = input('Password:')
    counter = 0
    data = {
        'username' : username,
        'password' : password
    }
    response = payload('login','login',data)

    if 'token' in response.keys():
        print(response['response'])
        return [True,response['token']]

    elif counter == 0:
        print('Huh, did he forget to give you the username and password?')
        print('Aw shucks, but hey! You two are good friends, SURELY you can think of something')
        print('His mind is quite simple, think of something related to the two of you...')
        login()

    else:
        print(response['response'])
        login()



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
            print(response[0])
            print("Want to try someone else?(yes/no)")
            looking_up(input(),token)

        return True

    elif look_up.lower() == 'no':
        print('Okie, your choice!')
        return True

    else:
        response = payload('login','douche',token)
        print(response['response'])
        looking_up(input('Now, be kind enough to give a proper answer :)\n(yes/no)'),token)
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


def get_level(token):
    print("What level would you like?")
    counter = 1
    for x in payload('main','find_levels', {'token': token}):
        print(str(counter) + x)
        counter += 1

    level = input('Enter the level you\'d want:')
    return level


def get_recipe(recipe,token):
    data = {
        'token' : token,
        'recipe' : recipe
    }
    return payload('main','find_recipe',data)


def parser(instructions):
    new_instructions = list(instructions)
    value = nth_index(new_instructions,'\n',2)
    print(''.join(new_instructions[:value]))
    new_instructions = new_instructions[value:]

    for x in range(75,len(new_instructions),75):
        if new_instructions[x] == ' ':
            print(''.join(new_instructions[x-75,x]))
        else:
            new_instructions.insert(x,'-')
            print(''.join(new_instructions[x-75,x]))
        input()

    return True

def print_recipe(recipe):
    print("[Level: {}]".format(recipe['level']))
    print("\\\\\\\\Torture level: {}/9000\\\\\\\\".format(recipe['level_of_torture']))
    print("Recipe {}: {}".format(recipe['index_of_recipe'],recipe['recipe_name']))
    print("[Ingredients]")
    parser(recipe['instructions'])


def actual_main(token):
    print('Would you like to take a look at someone specific?(yes/no)')
    look_up = input()
    looked = looking_up(look_up, token)

    if isinstance(looked, str):
        level = get_level(token)
        recipes = offered_recipes(token, level, looked)
    else:
        level = get_level(token)
        recipes = offered_recipes(token, level)

    print(recipes['welcome_response'])
    counter = 1
    for x in recipes['response']:
        print(str(counter) + x)
        counter += 1

    recipe_name = input("What shall we have:")
    if str.isdigit(recipe_name):
        recipe = get_recipe(recipes[int(recipe_name) - 1], token)
    else:
        recipe = get_recipe(recipe_name, token)

    finished = print_recipe(recipe)
    if finished:
        another = input("Want to go again?")
        if another.lower() == 'yes':
            actual_main(token)
        else:
            print("Thank you for coming, hope we see you back soon!")
            time.sleep(30)

def main():
    print('Why hello there, i see you\'re a close friend of Pazzio\'s!')
    details = login()
    token = details[1]
    if details[0]:
        actual_main(token)


main()
