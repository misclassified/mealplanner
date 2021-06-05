from django.shortcuts import render
import numpy as np
import pandas as pd
import sys
import os

from .models import Recipe, Ingredients, Recipe_Fact
# Create your views here.

sys.path.append("../")
from utils import SqliteUtils

def home(request):
    return render(request, 'weekly_planner/home.html')

def test(request):
    return render(request, 'weekly_planner/test.html')


def planner(request):

    length = int(request.GET.get('recipes', 3))
    people = int(request.GET.get('people', 2))
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_local_path = os.path.join(BASE_DIR, 'db.sqlite3')

    sql = SqliteUtils(db_local_path)

    # Select recipes

    sql_query = """
            select rec.recipe_name, 
                   rec.url,
                   facts.ingredient,
                   facts.unit_measure,
                   facts.quantity
            from weekly_planner_recipe rec
            left join weekly_planner_recipe_fact facts
            using(recipe_name)
    """

    recipes = sql.sqlite_to_pandas(sql_query)
    rand_recipe_names = np.random.choice(recipes['recipe_name'].unique(),
                                    size=length, 
                                    replace=False)

    rand_recipes = recipes[recipes['recipe_name'].isin(rand_recipe_names)].copy()
    rand_recipes['quantity'] = rand_recipes['quantity'].astype(float)
    rand_recipes_agg = rand_recipes.groupby('recipe_name').agg({'ingredient': list,
                                              'url': max
                                            }).reset_index()

    # Fetch Ingredients
    recipe_dict = {}
    ingredient_tuples = []

    for rr in rand_recipes_agg.itertuples():

        recipe_dict[rr.recipe_name] = {'ingredients_list': ", ".join([x for x in rr.ingredient]),
                                       'ingredients_tuples': tuple(rr.ingredient),
                                       'url': rr.url}

    ingredient_tuples = rand_recipes. \
                  groupby(['ingredient', 'unit_measure']). \
                  agg({'quantity':np.sum}). \
                  reset_index()

    # Create Shopping list
    sl = ShoppingList(ingredient_tuples, people)
    shopping_list = sl.create_shopping_list()

    return render(request, 'weekly_planner/planner.html', {'recipes':recipe_dict, 
                                                           'shopping_list': shopping_list})



class ShoppingList(object):

    def __init__(self, ingredient_tuples, people):

        self.ingredient_tuples = ingredient_tuples
        self.people = people

    def create_shopping_list(self):

        # Group by ingredient and unit_measure
        ing_df = self.ingredient_tuples.groupby(['ingredient', 'unit_measure'], as_index=False).sum()
        ing_df = ing_df.sort_values(by = 'ingredient')
        ing_df = ing_df.set_index('ingredient')

        # Multiply quantities by number of people
        ing_df['quantity'] = ing_df['quantity'] * self.people

        # Round to nearest 10'
        ing_df['quantity'] = [x + (10-(x % 10)) 
                              if x % 10 > 0 
                              else x 
                              for x in ing_df['quantity']]

        # Convert to str and replace 0 values with empty string
        ing_df['quantity'] = ing_df['quantity'].astype('int').astype('str')
        ing_df['quantity'] = ing_df['quantity'].replace('0', ' ')

        # Replace nas in unite unit measure with empty string
        ing_df['unit_measure'] = ing_df['unit_measure'].astype('str')
        ing_df['unit_measure'] = ing_df['unit_measure'].replace('nan', ' ')

        # Create ingredients list
        shopping_list = ing_df.transpose().to_dict()

        return shopping_list