from django.shortcuts import render
import numpy as np
import pandas as pd

from .models import Recipe, Ingredients, Recipe_Fact
# Create your views here.

def home(request):
    return render(request, 'weekly_planner/home.html')

def test(request):
    return render(request, 'weekly_planner/test.html')

def planner(request):

    length = int(request.GET.get('recipes', 3))
    people = int(request.GET.get('people', 2))

    recipes = Recipe.objects.all()
    rand_recipes = np.random.choice(recipes, size=length, replace=False)

    # Fetch Ingredients
    recipe_dict = {}
    ingredient_tuples = []

    for rr in rand_recipes:

        recipe_dict[rr.recipe_name] = {'ingredients_list': None,
                                       'ingredients_tuples': None,
                                       'url': rr.url}

        # For each selected recipe fetch ingredients
        recipe_facts = Recipe_Fact.objects.select_related('ingredient'
            ).filter(recipe_name=rr.recipe_name)

        recipe_ingredients = []

        for rec_fact in recipe_facts:
            recipe_ingredients.append((rec_fact.ingredient.ingredient,
                                      rec_fact.quantity,
                                      rec_fact.ingredient.unit_measure))

        recipe_dict[rr.recipe_name]['ingredients_list'] = ", ".join([x[0] for x in recipe_ingredients])
        ingredient_tuples.extend(recipe_ingredients)

    # Create Shopping list
    sl = ShoppingList(ingredient_tuples, people)
    shopping_list = sl.create_shopping_list()

    return render(request, 'weekly_planner/planner.html', {'recipes':recipe_dict, 'shopping_list': shopping_list})



class ShoppingList(object):

    def __init__(self, ingredient_tuples, people):

        self.ingredient_tuples = ingredient_tuples
        self.people = people

    def create_shopping_list(self):

        # Create Ingredients Pandas DataFrame
        vars = ['ingredient', 'quantity', 'unit_measure']
        ing_df = pd.DataFrame(self.ingredient_tuples, columns=vars)
        ing_df['quantity'] = ing_df['quantity'].astype(float).fillna(0)

        # Group by ingredient and unit_measure
        ing_df = ing_df.groupby(['ingredient', 'unit_measure'], as_index=False).sum()
        ing_df = ing_df.sort_values(by = 'ingredient')
        ing_df = ing_df.set_index('ingredient')

        # Multiply quantities by number of people
        ing_df['quantity'] = ing_df['quantity'] * self.people

        # Round to nearest 50'
        ing_df['quantity'] = [(x[0]+50 - (x[0] % 50)) if x[0] != 0 and x[1] != 'nan'
            else x[0] for x in zip(ing_df['quantity'], ing_df['unit_measure'])]
        print(ing_df[ing_df['unit_measure'] == 'nan'])

        # Convert to str and replace 0 values with empty string
        ing_df['quantity'] = ing_df['quantity'].astype('int').astype('str')
        ing_df['quantity'] = ing_df['quantity'].replace('0', ' ')

        # Replace nas in unite unit measure with empty string
        ing_df['unit_measure'] = ing_df['unit_measure'].astype('str')
        ing_df['unit_measure'] = ing_df['unit_measure'].replace('nan', ' ')

        # Create ingredients list
        shopping_list = ing_df.transpose().to_dict()

        return shopping_list
