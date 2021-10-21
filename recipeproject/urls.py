"""recipeproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from recipeapp.serializers.serializers import DirectionSerializer
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url
from recipeapp.views.home import home
from recipeapp.views.recipe import DirectionsViewSet, IngridientsViewSet, RatingsViewSet, RecipeViewSet, userviewsets
from mpesa.urls import mpesa_urls

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'rates', RatingsViewSet)
router.register(r'ingridients', IngridientsViewSet)
router.register(r'users', userviewsets)
router.register(r'methods', DirectionsViewSet,basename='Direction')





schema_view = get_schema_view(
   openapi.Info(
      title="RECIPE API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.ourapp.com/policies/terms/",
      contact=openapi.Contact(email="contact@classyrecipes.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)





urlpatterns = [
    path('admin/', admin.site.urls),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('',include('recipeapp.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
# path('api/v1/', include('mpesa.urls')),
 path('mpesa/', include(mpesa_urls)),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
# path('api/v1/', include('mpesa_api.urls')),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
