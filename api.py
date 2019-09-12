from login.models import *
from main.models import *

class UserAPI:

    def pair(class_type,text,*users,tmp_obj=None):
        if tmp_obj != None:
            obj = tmp_obj
        else:
            obj = class_type.objects.get(text__startswith=text)

        for tmp_user in users:
            try:
                user = User.objects.get(username=tmp_user)
            except:
                print(f"User '{tmp_user}' does not exist!")
                continue
            obj.user.add(user)
        return True


    def check_answer():
        answer = input("What type of a delete do you want?(delete/unpair)\n")
        if answer in ['delete','unpair']:
            return answer
        else:
            print("Choose a one of the offered answers!\n")
            return UserAPI.check_answer()
        

    def delete(class_type,text,*users,type=""):
        if type == "":
            type = UserAPI.check_answer()
        
        print(f"MODE:{type.upper()}")
        objects = class_type.objects.filter(text__startswith=text)
        while len(objects) != 0:
            answer = input(f"Do you want to {type} all of the copies of '{class_type.__name__}' with the text '{objects[0].text}' in the database?(yes/no)\n")
            tmp_obj = objects.filter(text = objects[0].text)
            if answer.lower() == "yes":
                objects = objects.exclude(id__in=tmp_obj)
                if type=="delete":
                    tmp_obj.delete()
                elif type=="unpair":
                    for user in users:
                        answer = input(f"Unpair from user '{user}'? (yes/no)\n")
                        if answer.lower() == "yes":

                            try:
                                real_user = User.objects.get(username=user)
                            except:
                                print(f"User '{user}' either does not exist, or there is more than one copy of them!")
                                continue
                            
                            for item in tmp_obj:
                                    item.user.remove(real_user)

            else:
                objects = objects.exclude(id__in = tmp_obj)

        return True

    
    def create(class_type,text,*users,type = ""):
        if len(class_type.objects.filter(text=text)) > 0:
            answer = input(f"The '{class_type.__name__}' with the text '{text}' already exists, are you sure you want to create another one?(yes/no)\n")
            if answer.lower() == "no":
                return

        obj = class_type.objects.create(text=text)
        if type != "":
            obj.type = type
            obj.save(update_fields=['type'])

        elif type == "" and class_type is Failed:
            obj.type = input("Type of fail:")
            obj.save(update_fields=['type'])

        if users != ():
            UserAPI.pair(class_type,text,*users,tmp_obj = obj)

        return True


    def create_user(username, password, name, *friends):
        return User.objects.create(username = username, password = password, name = name, friends = list(friends))
