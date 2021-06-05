from django.db import models


# Create your models here.

class Recipe(models.Model):

    recipe_name = models.CharField(max_length=100, primary_key=True, db_column='recipe_name')
    recipe_source = models.CharField(max_length=100, db_column='recipe_source')
    url = models.URLField(max_length=200, db_column='url')
    timestamp = models.DateTimeField(auto_now=True, db_column='timestamp')

    def __str__(self):
        return (self.recipe_name)


class Ingredients(models.Model):
    
    ingredient_id = models.CharField(max_length=100, primary_key=True, db_column='ingredient_id')
    ingredient = models.CharField(max_length=50, db_column='ingredient')
    unit_measure = models.CharField(max_length=20, db_column='unit_measure')
    timestamp = models.DateTimeField(auto_now=True, db_column='timestamp')

    def __str__(self):
        return (self.ingredient_id)


class Recipe_Fact(models.Model):

    recipe_name = models.ForeignKey(Recipe, on_delete=models.CASCADE, db_column='recipe_name')
    ingredient_id = models.ForeignKey(Ingredients, on_delete=models.CASCADE, db_column='ingredient_id')
    ingredient = models.CharField(max_length=50, db_column='ingredient')
    unit_measure = models.CharField(max_length=20, null = True, db_column='unit_measure')
    quantity = models.IntegerField(db_column = 'quantity')
    timestamp = models.DateTimeField(auto_now=True, db_column = 'timestamp')

    def __str__(self):
        return ('{}_{}'.format(self.recipe_name, self.ingredient))
