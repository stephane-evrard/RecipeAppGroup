from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from .models import UserProfile


def user_profile(request, username):
    """
    Displays the user profile of the user with the specified username.
    """
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.get_or_create(user)
    errors = request.session.pop('form_errors', None)
    context = {'profile': profile, 'form_errors': errors, 'explore': 'user_profile'}
    return render(request, 'core/users/user_profile.html', context)
