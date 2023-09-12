from django.contrib import admin
from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path("attraction", views.add_attraction, name= "add_attraction"),
    path("night-life", views.night_life, name= "night_life"),
    
]