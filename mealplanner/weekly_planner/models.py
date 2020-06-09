from django.db import models


# Create your models here.

class Recipe(models.Model):

    RECIPE_SOURCES = (
        ('GF', 'Giallo Zafferano'),
        ('MY', 'Mysia'),
        )

    recipe_name = models.CharField(max_length=100, primary_key=True)
    recipe_source = models.CharField(max_length=100, choices=RECIPE_SOURCES)
    url = models.URLField(max_length=200)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.recipe_name)


class Ingredients(models.Model):

    UNIT_MEASURES = (
            ('gr', 'grams'),
            ('ml', 'milliliters'),
            ('kg', 'kilograms'),
            ('lt', 'litre'),
            (' ',  'unit')
            )

    ingredient = models.CharField(max_length=50, primary_key=True)
    unit_measure = models.CharField(max_length=20, null=True, choices=UNIT_MEASURES)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.ingredient)


class Recipe_Fact(models.Model):

    recipe_name = models.ForeignKey(Recipe, on_delete=models.CASCADE, db_column='recipe_name')
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE, db_column='ingredient')
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ('{}_{}'.format(self.recipe_name, self.ingredient))
