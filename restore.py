# -*- coding: utf-8 -*-

path = "back\\testing"
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Oceni.settings")
django.setup()

import csv

from main.models import *
from login.models import *

from django.db import transaction

import itertools
import threading
import time
import sys

def animation(done):
    def animate():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\rloading ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\rDone!     \n')

    t = threading.Thread(target=animate)
    t.setDaemon(True)
    t.start()

    #long process here
    time.sleep(30)
    done = True
    


def restore_users():
    data = csv.DictReader(open(path + "/user.csv", encoding='utf-8'))
    counter = 0
    full_counter = 0
    with transaction.atomic(using=db_type):
        for row in data:
            if counter == 100:
                animation(False)
                counter = 0
            
            try:
                user = User.objects.get(name=row['name'])
            except:
                user = User.objects.create(id=row['id'])

            for attr,val in row.items():
                setattr(user,attr,val)

            user.save(using=db_type)

        counter += 1
        full_counter += 1

        print(str(full_counter) + "   ////  " + str(user))

def restore_intros():
    data = csv.DictReader(open(path + "/intro.csv", encoding='utf-8'))
    user = User.objects.get(username="honest")
    counter = 0
    full_counter = 0
    with transaction.atomic(using=db_type):
        for row in data:
            if counter == 100:
                animation(False)
                counter = 0
            
            try:
                intro = Intro.objects.get(name=row['text'])
            except:
                intro = Intro.objects.create(id=row['id'])

            for attr,val in row.items():
                setattr(intro,attr,val)

            intro.user.add(user)

            intro.save(using=db_type)

        counter += 1
        full_counter += 1

        print(str(full_counter) + "   ////  " + str(intro))
        
def restore_failed():
    data = csv.DictReader(open(path + "/failed.csv", encoding='utf-8'))
    user = User.objects.get(username="honest")
    counter = 0
    full_counter = 0
    with transaction.atomic(using=db_type):
        for row in data:
            if counter == 100:
                animation(False)
                counter = 0
            
            try:
                failed = Failed.objects.get(name=row['text'])
            except:
                failed = Failed.objects.create(id=row['id'])

            for attr,val in row.items():
                setattr(failed,attr,val)

            failed.user.add(user)

            failed.save(using=db_type)

        counter += 1
        full_counter += 1

        print(str(full_counter) + "   ////  " + str(failed))
        
def restore_responses():
    data = csv.DictReader(open(path + "/responses.csv", encoding='utf-8'))
    user = User.objects.get(username="honest")
    counter = 0
    full_counter = 0
    with transaction.atomic(using=db_type):
        for row in data:
            if counter == 100:
                animation(False)
                counter = 0
            
            try:
                response = Responses.objects.get(name=row['text'])
            except:
                response = Responses.objects.create(id=row['id'])

            for attr,val in row.items():
                setattr(response,attr,val)

            response.user.add(user)

            response.save(using=db_type)

        counter += 1
        full_counter += 1

        print(str(full_counter) + "   ////  " + str(response))
        
def restore_level():
    data = csv.DictReader(open(path + "/level.csv", encoding='utf-8'))
    #recipe = Recipe.objects.all().first()
    user = User.objects.get(username="honest")
    counter = 0
    full_counter = 0
    with transaction.atomic(using=db_type):
        for row in data:
            if counter == 100:
                animation(False)
                counter = 0
            
            try:
                level = Level.objects.get(name=row['name'])
            except:
                level = Level.objects.create(id=row['id'])

            for attr,val in row.items():
                setattr(response,attr,val)

            #level.user.add(user)

            level.save(using=db_type)

        counter += 1
        full_counter += 1

        print(str(full_counter) + "   ////  " + str(level))

def restore_recipes():
    data = csv.DictReader(open(path + "/recipe.csv", encoding='utf-8'))
    user = User.objects.get(username="honest")
    counter = 0
    full_counter = 0
    with transaction.atomic(using=db_type):
        for row in data:
            if counter == 100:
                animation(False)
                counter = 0
            
            try:
                recipe = Recipe.objects.get(name=row['name'])
            except:
                recipe = Recipe.objects.create(id=row['id'])

            for attr,val in row.items():
                setattr(recipe,attr,val)

            recipe.user.add(user)
            recipe.save(using=db_type)

        counter += 1
        full_counter += 1

        print(str(full_counter) + "   ////  " + str(recipe))

def restore_ingredients():
    data = csv.DictReader(open(path + "/ingredient.csv", encoding='utf-8'))
    recipe = Recipe.objects.all().first()
    user = User.objects.get(username="honest")
    counter = 0
    full_counter = 0
    with transaction.atomic(using=db_type):
        for row in data:
            if counter == 100:
                animation(False)
                counter = 0
            
            try:
                ingredient = Ingredient.objects.get(name=row['name'])
            except:
                ingredient = Ingredient.objects.create(id=row['id'])

            for attr,val in row.items():
                setattr(ingredient,attr,val)

            ingredient.recipes.add(recipe)
            ingredient.save(using=db_type)

        counter += 1
        full_counter += 1

        print(str(full_counter) + "   ////  " + str(ingredient))

def restore_category():
    data = csv.DictReader(open(path + "/ingredient.csv", encoding='utf-8'))
    recipe = Recipe.objects.all().first()
    user = User.objects.get(username="honest")
    counter = 0
    full_counter = 0
    with transaction.atomic(using=db_type):
        for row in data:
            if counter == 100:
                animation(False)
                counter = 0
            
            try:
                ingredient = Ingredient.objects.get(name=row['name'])
            except:
                ingredient = Ingredient.objects.create(id=row['id'])

            for attr,val in row.items():
                setattr(ingredient,attr,val)

            ingredient.recipes.add(recipe)
            ingredient.save(using=db_type)

        counter += 1
        full_counter += 1

        print(str(full_counter) + "   ////  " + str(recipe))


