from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from star_ratings.models import Rating
from recipeapp.models.models import Direction, Ingredient, Recipe

class userSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  '__all__'
# Serializers define the API representation.
class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    directions = serializers.SerializerMethodField()

    @staticmethod
    def get_ingredients(model):
        res = []
        for ing in model.ingredient_set.all():
            res.append({'name': ing.ingredient.name, 'quantity': ing.quantity, 'index': ing.index})
        return res

    @staticmethod
    def get_directions(model):
        res = []
        for direction in model.direction_set.all():
            res.append({'text': direction.text, 'index': direction.index})
        return res
    class Meta:
        model = Recipe
        fields = (
            'created_at', 'user', 'name','image',  'summary', 'prep_time', 'cook_time', 'servings', 'calories',
            'is_featured',  'ingredients', 'directions', 
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'







       