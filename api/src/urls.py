"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def home_view(request):
    return JsonResponse({"message": "Welcome to the API"})

urlpatterns = [
    path('', home_view, name='home'),  # Nouvelle route racine
    path('admin/', admin.site.urls),  # Modifié pour inclure le préfixe 'api'
    path('api/base/', include('base.urls')),
    path('api/auth/', include ('Auth.urls')),
]
