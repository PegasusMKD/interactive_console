from .models import *
from login.models import User,Failed
import json
import random

"""

Output for offering the recipes:
Welcome:
1. recipe 1
2. recipe 2
3. recipe 3
.
.
.



{
'recipe 1' : {
    'level' : 'expert',
    'level_of_torture' : 2000,
    'index_of_recipe' : 1548,
    'ingredients' : [['ingredient 1',2],['ingredient 2',1]...],
    'instructions' : 'text text'
    }
}


Output for recipe:
[Level Expert: expert]
\\\\Torture level: 2000/9000\\\\
Recipe 1548: recipe 1
    [Ingredients]
    2x ingredient 1 
    1x ingredient 2


    Today's dish is prepared with the finest of bobs!
    It starts with a cool heating of plastic at 275°C.
    Next step is ofcourse, setting up your bob to the
    torture chair! After you've done that, you start 
    pouring it all into his anal opening. Afterwards,
    you should let it cool-off for a while so it be-
    comes stiff....


legend for recipe instructions:
[ingredient expression] - to know if should go with full fix
$ - ingredients so that $1 is the first ingredient, $3 is the third ingredient
& - ammount of the ingredient so that &1 is the first ingredient, &3 is the third ingredient
() - category of ingredient so that (1) is the first ingredient, (3) is the third ingredient
%%% - name of the bob
@* - name of user
!^ - name of friend so that !^1 is first friend, !^2 is second friend
"""

"""
Extras
"""

def replacer(to_replace,friends=[],ingredients=[],bob="",user=""):
    string = ""
    print(friends)
    print(bob)
    print(user)
    print(to_replace.split())
    switcher = False
    second_switcher = False
    for x in to_replace.split():

        if x == '[' or switcher is True:
            if switcher is False:
                switcher = True
                continue

            if '&' in x:
                string += str(ingredients[int(''.join([y for y in x if str.isdigit(y)])) - 1][1]) + "x "
            elif '$' in x:
                string += str(ingredients[int(''.join([y for y in x if str.isdigit(y)])) - 1][0]) + " "
            elif '(' in x:
                string += '(' + ingredients[int(''.join([y for y in x if str.isdigit(y)])) - 1][2] + ')\n '
            else:
                string += "\n\n " + x + " "
                switcher=False


        elif x==">" or second_switcher is True:
            if second_switcher is False:
                second_switcher = True
                continue
            if '&' in x:
                string += str(ingredients[int(''.join([y for y in x if str.isdigit(y)])) - 1][1]) + "x "
            elif '$' in x:
                string += str(ingredients[int(''.join([y for y in x if str.isdigit(y)])) - 1][0]) + " "
            elif '(' in x:
                string += '(' + ingredients[int(''.join([y for y in x if str.isdigit(y)])) - 1][2] + ') '
            else:
                string += x + " "
                second_switcher = False



        elif '!^' in x:
            string += friends[int(''.join([y for y in x if str.isdigit(y)])) - 1] + " "
        elif '@*' in x:
            string += user + " "
        elif '%%%' in x:
            string += bob + " "
        else:
            string += x + " "

    return string



"""
Main funcs
"""
def offering_recipes(request):
    req = json.loads(request.body)
    user = User.objects.get(token=req['token'])

    try:
        tmp_recipes = Recipe.objects.filter(user__recognized=req['recognized'],level__name=req['level'])
        if len(tmp_recipes.all()) == 0:
            return json.dumps({
                'response': random.choice(Failed.objects.filter(type='empty')).text  # 'Утнат user, sowwie >,<'
            })
        recipes = [random.choice(tmp_recipes.all()) for x in range(5)]
    except:
        tmp_recipes = Level.objects.get(name=req['level']).lvl_recipes
        if len(tmp_recipes.all()) == 0:
            return json.dumps({
                'response': random.choice(Failed.objects.filter(type='empty')).text  # 'Утнат user, sowwie >,<'
            })
        recipes = [random.choice(tmp_recipes.all()) for x in range(5)]

    all_recipes = []
    for x in recipes:
        all_recipes.append(x.name)

    return json.dumps({
        'welcome_response' : random.choice(user.intros.all()).text,
        'response' : all_recipes
    })




def find_recipe(request):
    req = json.loads(request.body)
    user = User.objects.get(token=req['token'])
    recipe = Recipe.objects.get(name=req['recipe'])

    ingredients = [[x.name,y,','.join([z.name for z in x.category.all().iterator()])] for x,y in zip(recipe.ingredients.all().iterator(),recipe.ingredient_ammount)]


    actual_recipe = {
        'recipe_name' : recipe.name,
        'level' : recipe.level.name,
        'level_of_torture' : recipe.level_of_torture,
        'index_of_recipe' : recipe.index_of_recipe,
        'instructions' : replacer(recipe.instructions,user.friends,ingredients,recipe.user,user.name),

    }
    print(recipe.instructions)
    print(actual_recipe)
    return json.dumps(actual_recipe)


def found_levels(request):
    req = json.loads(request.body)
    user = User.objects.get(token=req['token'])
    print([x.name for x in Level.objects.all()])
    return json.dumps({
        'levels' : [x.name for x in Level.objects.all()]
    })