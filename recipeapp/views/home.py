import json
from django.http.response import HttpResponseRedirect
import requests
import logging
from os import sync

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import context
from recipeapp.forms.recipe import ReviewForm
from django.core.mail import send_mail
from recipeapp.models.models import LNmpesaOnline, Recipe, Review, UserProfile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from recipeapp.views.mpesa_credentials import LipanaMpesaPpassword, MpesaAccessToken

def home(request):
   
    try:
        query = request.GET.get('q')    
        recipes=Recipe.search(query)
        print(query)
        context={
            'recipe':recipes,
            
        }
        
    except:
        if request.user.id:
            
            profile=UserProfile.objects.get(user_id=request.user.id)
            phone=profile.PhoneNumber
            phone=str(phone)
            print(phone)
            phone=phone[1:]
            phone=str(phone)
            pre='254'
            phone=(pre+phone)
            upgrade=LNmpesaOnline.objects.filter(PhoneNumber=profile.PhoneNumber,Amount=1.0)
            recipe=Recipe.objects.all().order_by('created_at').reverse()
            print(upgrade)   
            

        
    
            recipe=Recipe.objects.all().order_by('created_at').reverse()
            
            context={
                'recipe':recipe,
                'upgrade':upgrade,
            }
        else:
            recipe=Recipe.objects.all().order_by('created_at').reverse()
            
            context={
                'recipe':recipe,
                
            }

    
    
    return render(request,'home/home.html',context)
def filter_recipes(request,what):
    recent=Recipe.filter_by_recent()
    ratings=Recipe.filter_by_rating()
    country=Recipe.filter_by_country()
    all=Recipe.objects.all().order_by('created_at').reverse()
    if what=='recent':
         context={
            'recipe':recent
        }
    elif what=='ratings':
        context={
            'recipe':ratings
        }
    elif what=='country':
        context={
            'recipe':country
        }
    else:
        context={
            'recipe':all
        }
    return render(request ,'home/home.html',context)


 
       
   
    
    return render(request,'home/home.html',context)


def viewpage(request,recipe_id):
    """
    Displays a detailed view of the recipes as specified in the URL.
    """
    profile=UserProfile.objects.get(user_id=request.user.id)
    phone=profile.PhoneNumber
     
    upgrade=LNmpesaOnline.objects.filter(PhoneNumber=profile.PhoneNumber,Amount=1.0)
    form=ReviewForm()
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.free==True or len(upgrade)>0:
        ingredients = recipe.ingredient_set.order_by('-index')
        directions = recipe.direction_set.order_by('-index')
        comments=Review.objects.filter(recipe=recipe_id)
        context = {
            'recipe': recipe,
            'ingredients': ingredients,
            'directions': directions,
            'form':form,
            'comments':comments
            
        }
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request,'core/rec_details.html',context)
@login_required()
def user_dashboard(request):
    return render(request, 'home/dashboard.html')
