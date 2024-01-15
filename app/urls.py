from django.contrib import admin
from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path("ai-bot", views.ai_bot, name= "ai_bot"),
    path("chat-with-ai", views.chat_with_ai, name= "chat_with_ai"),
    path("night-life", views.night_life, name= "night_life"),
    
]
