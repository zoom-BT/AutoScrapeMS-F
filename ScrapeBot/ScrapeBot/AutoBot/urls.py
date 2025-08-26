"""
URL configuration for AutoBot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from AutoBot.Scrape.views import home, scrape_view, scrape_affiche, scrape_export, scrape_planifie, register_email, register, user_login, user_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('scrape/', scrape_view, name='scrape'),
    path('affiche/', scrape_affiche, name='affiche'),
    path('export/', scrape_export, name='export'),
    path('planifie/', scrape_planifie, name='planifie'),
    path('register_email/', register_email, name='register_email'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
