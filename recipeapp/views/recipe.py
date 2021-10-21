from datetime import datetime, timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import routers, serializers, viewsets
from django.views.generic.list import ListView
from star_ratings.models import Rating
from recipeapp.forms.recipe import  ReviewForm, SubmitRecipeForm
from recipeapp.models.models import Direction, Ingredient, Recipe, Review
from recipeapp.serializers.serializers import  userSerializers,DirectionSerializer, IngredientSerializer, RatingSerializer, RecipeSerializer
from django.core.mail import send_mail
from rest_framework import viewsets
 
from django.contrib.auth.models import User

def submit_recipe(request):
    """
    Submits a new recipes for creation.
    """
    if request.method == 'POST':
        form = SubmitRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            
            recipe.save()
            form.save_ingredients(recipe)
            form.save_directions(recipe)
            send_mail('You edited a recipe', 'Thank you for contributing to our app.You posted a recipe at classy recipe  <br/>Regards,  <br/>Mwashe Berit', 'mwasheberit@gmail.com', [request.user.email], fail_silently=False)
            return redirect('/')
    else:
        form = SubmitRecipeForm()
    return render(request,'adds/recipe_submit.html' ,{'form':form})

def favorite_add(request,recipe_id):
    post=get_object_or_404(Recipe,id=recipe_id)
    if post.favorites.filter(id=request.user.id).exists():
        post.favorites.remove(request.user)
       
    else:
        post.favorites.add(request.user)
    return redirect('favorite_list') 
 
def favorite_list(request):
    new= Recipe.objects.filter(favorites=request.user)
    
    return render(request,'core/favorites.html',{'new':new})

def delete_recipe(request, recipe_id):
    recipe_id = int(recipe_id)
    try:
        recipe_sel = Recipe.objects.get(id = recipe_id)
    except:
        return redirect('/')
    recipe_sel.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required
def edit_recipe(request, recipe_id):
    """
    Submits changes to an already created recipe.
    """
    recipe_to_edit = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = recipe_to_edit.ingredient_set.order_by('-index')
    directions = recipe_to_edit.direction_set.order_by('-index')
    
    print(recipe_to_edit)
    if request.user != recipe_to_edit.user:
        return HttpResponseForbidden()
    else:
        if request.method=='POST':
            recipe_to_edit = get_object_or_404(Recipe, pk=recipe_id)
            form = SubmitRecipeForm(request.POST, request.FILES,instance=recipe_to_edit)
            if form.is_valid():
                recipe = form.save(commit=False)
                recipe.user = request.user
                
                
                recipe.save()
                
                form.save_ingredients(recipe)
                form.save_directions(recipe)
                return redirect('/')
        else:
                recipe_to_edit = get_object_or_404(Recipe, pk=recipe_id)
                form = SubmitRecipeForm(request.POST, request.FILES,instance=recipe_to_edit)
    return render(request,'core/recipe_submit.html',{'form':form,'recipe':recipe_to_edit,'ingridients':ingredients,'directions':directions})


@login_required
def submit_review(request, recipe_id):
    """
    Submits a review for the recipes as specified in the URL.
    """
   
    user=User.objects.get(id=request.user.id)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        
       
        if form.is_valid():
           
            print('yes')
            rvw = form.save(commit=False)
            rvw.user=user
           
            rvw.recipe = recipe
            rvw.save()
            
            return redirect('/')
        else:
            print('no')
   

    return redirect(request.META.get('HTTP_REFERER'))

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class DirectionsViewSet(viewsets.ModelViewSet):
    queryset =  Direction.objects.all()
    serializer_class = DirectionSerializer


class RatingsViewSet(viewsets.ModelViewSet):
    queryset =  Rating.objects.all()
    serializer_class = RatingSerializer



class IngridientsViewSet(viewsets.ModelViewSet):
    queryset =  Ingredient.objects.all()
    serializer_class = IngredientSerializer



class userviewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializers



