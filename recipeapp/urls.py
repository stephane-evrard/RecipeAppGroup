from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from recipeapp.views import home,recipe,usars,views,paypal,mpesa



urlpatterns = [
  path('',home.home,name='home'),
  path('search',home.home,name='search'),
  path('viewpage/<int:recipe_id>',home.viewpage,name='viewpage'),
  path('fav/<int:recipe_id>',recipe.favorite_add,name='fav'),
  path('submit',recipe.submit_recipe,name='submit_recipe'),
  path('profile/favorites',recipe.favorite_list,name='favorite_list'),
  path('filter_recipe/<str:what>/',home.filter_recipes,name='filter_recipe'),
  path('recipe_delete/<int:recipe_id>/delete', recipe.delete_recipe, name='delete'),
  path('recipes/<int:recipe_id>/edit', recipe.edit_recipe, name='edit_recipe'),
  path('users/<username>/', usars.user_profile, name='user_profile'),
  path('editprofile',usars.edit_profile,name='edit_profile'),
  path('recipes/<int:recipe_id>/comment',recipe.submit_review,name='comment'),
  path('dashboard', home.user_dashboard, name='user_dashboard'),
  path('signup', views.signup, name='signup'),
  path('activate/<uidb64>/<token>', views.activate, name='activate'),
  path('signin', views.signin, name='signin'),
  path('signout', views.signout, name='signout'),
  path('lnm', mpesa.LnmOnlinecallbackurlView.as_view(), name='lnm'),
  path('access_token',mpesa.getAccessToken,name='access_token'),
  path('online/lipa/', mpesa.lipa_na_mpesa_online, name='lipa_na_mpesa'),





  

]
