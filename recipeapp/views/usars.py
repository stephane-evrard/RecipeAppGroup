from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from recipeapp.forms.users import SaveUserProfileForm

from recipeapp.models.models import UserProfile


def user_profile(request, username):
    """
    Displays the user profile of the user with the specified username.
    """
    
    user = get_object_or_404(User, username=username)
    profile=UserProfile.objects.get(user_id=user.id)
    errors = request.session.pop('form_errors', None)
    user = get_object_or_404(User, username=username)
    recipes = user.recipe_set.all()
    context = {'profile': profile, 'form_errors': errors, 'explore': 'user_profile','recipe_list': recipes, 'user': user, 'explore': 'user_recipes'}
    return render(request, 'profile/user_profile.html', context)


def edit_profile(request):
        profile=UserProfile.objects.get(user_id=request.user.id)
        if request.method == 'POST':
           
            profile_form = SaveUserProfileForm(request.POST, request.FILES,instance=profile)
            if  profile_form.is_valid():
               
             
                profile_form.save()
                return redirect('/')
               
           
                
        else:
         
            profile_form =SaveUserProfileForm(instance=profile)
        return render(request, 'profile/edit_prof.html', {
        # 'user_form': user_form,
        'form': profile_form
    })
    
           
          