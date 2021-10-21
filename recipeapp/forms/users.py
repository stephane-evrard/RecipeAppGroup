from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from recipeapp.models.models import UserProfile, IngredientName, Recipe, Ingredient

class SaveUserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('image', 'bio')