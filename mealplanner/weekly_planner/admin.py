from django.contrib import admin
from .models import Recipe, Ingredients, Recipe_Fact

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Ingredients)
admin.site.register(Recipe_Fact)
