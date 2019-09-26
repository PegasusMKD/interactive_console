import requests
import json
from itertools import islice
import time

import msvcrt as m

import warnings
from urllib3.exceptions import  InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)

"""
Extras
"""
def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)

def wait():
    m.getch()

def payload(url,path,payload={}):
     request = requests.post('https://theboble.herokuapp.com/{}/{}/'.format(url,path),headers={'content-type' : 'application/json'},data=json.dumps(payload))
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


def get_chapters(token,option):
    data = {
            'token' : token,
            'option' : option,
        }

    return payload('game','get_chapters', data)

def return_int(val):
    return int(val.split(" ")[1][0])

def get_options(token,last_options = []):
    print("What option would you like?")
    counter = 1
    if last_options == []:
        options = payload('game','get_options', {'token': token})['options']
    else: 
        options = last_options

    for x in options:
        print(str(counter) + '. ' + x)
        counter += 1

    option = input('Enter the option you\'d want:')
    if str.isdigit(option):
        if 0 < int(option) > len(options):
            print("Alo shmekeri, ona nije moja!")
            return get_options(token,options)
        else:
            return options[int(option)-1]

    elif option in options:
        return option
    else:
        return False


def get_chapter(chapter, option, token):
    data = {
        'token' : token,
        'option' : option,
        'chapter' : chapter
    }
    return payload('game','get_chapter',data)


def new_parser(instructions):
    tmp_list = instructions.split(" ")
    line = []
    counter = 0
    for word in tmp_list:
        if '\n' in word:
            line.append(word)
            print(' '.join(line))
            counter = 0
            line =[]
            wait()
        elif counter <= 65:
            line.append(word)
            counter += len(word)
        else:
            line.append(word)
            print(' '.join(line))
            counter = 0
            line = []
            wait()
    print(' '.join(line))
    return True


def got_correct(token):
    data = {
        'token' : token,
        }

    return payload('game', 'got_correct', data)

def print_chapter(token, chapter):
    bar = '=' * 85
    bar = list(bar)
    for idx,character in enumerate([' '] + list(chapter['title']) + [' ']):
        bar[8+idx] = character

    print(''.join(bar) + '\n')
    new_parser(chapter['text'])
    answer = input("\nQuestion: " + chapter['question'] + "\n").capitalize()
    if answer == chapter['answer'].lower():
        print(got_correct(token)['response'])

    return True


def actual_main(token):
    option, chapters = offer_chapters(token)
    print()
    print(chapters['welcome_response'])
    counter = 1
    if option != "Rules":
        chapters['response'] = sorted(chapters['response'],key=return_int)

    for x in chapters['response']:
        print(str(counter) + '. ' + x)
        counter += 1

    chapter = chapters_loop(chapters, option, token)
    print()
    finished = print_chapter(token, chapter)
    print()

    if finished:
        another = input("Want to go again? (yes/no)\n")
        if another.lower() == 'yes':
            actual_main(token)
        else:
            print("Thank you for coming, hope we see you back soon!")
            time.sleep(30)


def chapters_loop(chapters, option, token):
    chapter_name = input("What shall we have:")
    if str.isdigit(chapter_name):
        if 0 < int(chapter_name) > len(chapters['response']):
            print("Nice tryy ~(0.0)~")
            chapter = chapters_loop(chapters, option, token)

        else:
            chapter = get_chapter(chapters['response'][int(chapter_name) - 1], option, token)

    elif chapter_name in chapters['response']:
        chapter = get_chapter(chapter_name, option, token)
    else:
        print("Not a shmart move, i must say...")
        chapter = chapters_loop(chapters, option, token)
    return chapter


def offer_chapters(token):

    option = get_options(token)
    if option is not False:
        chapters = get_chapters(token, option)
        if not isinstance(chapters['response'],list):
            print(chapters['response'])
            return offer_chapters(token)
    else:
        return offer_chapters(token)

    return option, chapters


def main():
    print('Why hello there, i see you\'re a close friend of Pazzio\'s!')
    details = login()
    token = details[1]
    type = details[2]
    if details[0]:
        actual_main(token)

main()