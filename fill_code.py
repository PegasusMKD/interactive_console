import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "The_Boble.settings")
django.setup()

from game.models import *

with open('code.txt','r+') as f:
    lines = f.readlines()
    counter = -1
    title =[]
    description =[]
    code = []
    chapter = []

    for line in lines:
        print(line)
        if line[:-1] in ["....", "//","AWESD","ANSWER","REWARD"]:
            print(line)
            counter += 1
            continue
        elif line[:-1] == "BBNO$":
            counter += 1

        if counter == -1:
            chapter.extend(list(line))

        if counter == 0:
            title.extend(list(line))

        elif counter == 1:
            description.extend(list(line))

        elif counter == 2:
            code.extend(list(line))
            
        elif counter == 3:
            answer = line

        elif counter == 4:
            reward = line

        elif counter == 5:
            print(chapter)
            chapter_obj = Chapter.objects.get(title=''.join(chapter[:-1]))
            exercise = Exercises.objects.get_or_create(chapter=chapter_obj,
                                    title = ''.join(title[:-1]),sample_code = ''.join(code),
                                    description=''.join(description[:-1]),answer=answer[:-1],
                                    reward=reward[:-1] )
            counter = -1
            title =[]
            description =[]
            code = []
            chapter = []
            print(exercise)
