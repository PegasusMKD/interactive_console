import typing
import random

from login.models import *
from main.models import *

class UserAPI:
    """
    API for easy creating, deleting, pairing and unpairing of models
    in the login module/app of the project
    """
    pair_users = typing.NewType("Positional arguments for each User",typing.List[str])
    create__users = typing.NewType('Tuple of usernames of users given as positional arguments to be paired with the object created',typing.List[str])
    delete__users = typing.NewType("Positional arguments for unpairing relations with a user",typing.List[str])
    star = typing.NewType('Tuple of friends given as positional arguments',typing.List[str])

    def pair(class_type,text: str,*users: pair_users,tmp_obj=None) -> bool:

        """
        Fuction which pairs up one login object, to a user, or more users, depending on the given parameters
        """

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


    def check_answer() -> str:
        
        """
        Checks if the answer given is valid, 
        if not it asks it again until a proper answer is given
        """

        answer = input("What type of a delete do you want?(delete/unpair)\n")
        if answer in ['delete','unpair']:
            return answer
        else:
            print("Choose a one of the offered answers!\n")
            return UserAPI.check_answer()
        

    def delete(class_type,text: str,*users: delete__users):

        """
        If no positional arguments for users has been given, then it deletes the items with the given model, 
        and same starting text as the one given as a parameter
        and if there are positional arguments for users, then it unapirs the items from those users.
        """
        
        if users == ():
            type = "delete"
        else:
            type = "unpair"
        
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

    
    def create(class_type,text:str,*users:create__users,type = ""):
        
        """
        Function which creates an object of the model given in class_type
        and pairs it up with the given users
        """

        if len(class_type.objects.filter(text=text)) > 0:
            answer = input(f"The '{class_type.__name__}' with the text '{text}' already exists, are you sure you want to create another one?(yes/no)\n")
            if answer.lower() == "no":
                return

        obj = class_type.objects.create(text=text)
        if type != "":
            obj.type = type
            obj.save(update_fields=['type'])

        elif type == "" and class_type is Failed:
            print("If you want to avoid this prompt, set the 'type' parameter.")
            obj.type = input("Type of fail:")
            obj.save(update_fields=['type'])

        if users != ():
            UserAPI.pair(class_type,text,*users,tmp_obj = obj)

        return True


    def create_user(username:str, password:str, name:str, *friends:star):
        """
        Creates a user
        """
        return User.objects.create(username = username, password = password, name = name, friends = list(friends))



class RecipeAPI:
    """
    API for easy creating, deleting, pairing and unpairing of models
    in the main module/app of the project
    """


    def pair(class_type,name: str,*users: '',tmp_obj=None) -> bool:

        """
        Fuction which pairs up one login object, to a user, or more users, depending on the given parameters
        """

        if tmp_obj != None:
            obj = tmp_obj
        else:
            obj = class_type.objects.get(name__startswith=name)

        for tmp_user in users:
            try:
                user = User.objects.get(username=tmp_user)
            except:
                print(f"User '{tmp_user}' does not exist!")
                continue
            obj.user.add(user)
        return True


    def create(class_type,name: str,*,category="") -> bool:

        obj = class_type.objects.create(name=name)

        if class_type is Ingredient:
            try:

                if category=="":
                    obj.category.add(Category.objects.get(name = input("Categories name:")))
                else:
                    obj.category.add(Category.objects.get(name = category))
            except:
                print("There is either more than one category with that name, or it does not exist")
                return
        elif class_type is Level:
            obj.max_level = input("Max level of torture:")
            obj.min_level = input("Min level of torture:")
            obj.save()
        return True


    def create_recipe(level,name,*users):
        lvl = Level.objects.get(name=level)
        recipe = Recipe.objects.create(level_id = lvl.id,level_of_torture = random.randint(lvl.min_level,lvl.max_level),index_of_recipe=random.randint(0,9999),name = name)

        print("What are the instructions for this recipe?")
        print("The legend goes like this:")
        print("Wrap the ingredients between '--' and '-', for example --ingredient--")
        print("Wrap the ingredient ammount between '!--' and '-', for example !--ingredient_ammount--!")
        #tmp_instructions = input()
        tmp_instructions = "|1| ingredient |1| needs <1>yeeteed<1> sadly."
        #word = []
        #counter = 0
        #max_ctr = 0
        #checker = True
        #main_check = True
        #for letter in tmp_instructions:
        #    if counter != max_ctr:
        #        print("counter")
        #        counter+=1
        #        main_check=True
        #        continue
        #    elif checker == False:
        #        main_check=False

        #    if (letter == '!' or letter == '-') and checker==True:
        #        checker = False
        #        main_check = True
        #        print("Got here")
            
        #    if letter == '!' and checker==False:
        #        if main_check == True:
        #            print("Izv")
        #            max_ctr += 2
        #            continue
        #        else:
        #            print("utepaj me")
        #            checker = True
        #            main_check=True
        #            continue

        #    elif letter=='-'  and checker==False:
        #        if main_check==True:
        #            print("crta")
        #            max_ctr += 1
        #            continue
        #        else:
        #            print("no u")
        #            checker = True
        #            main_check=True

        #            continue
            
        #    if main_check==False and checker==False:
        #        word.append(letter)

        reworked = tmp_instructions.split(' ')
        for idx,val in enumerate(reworked):
            if '|' in val:
                


