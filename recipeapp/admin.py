from django.contrib import admin

from recipeapp.models import models
# Register your models here.

admin.site.register(models.Recipe)
admin.site.register(models.Ingredient)
admin.site.register(models.Direction)
admin.site.register(models.UserProfile)

admin.site.register(models.IngredientName)
admin.site.register(models.Review)
admin.site.register(models.LNmpesaOnline)





