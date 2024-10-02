from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('chat/',views.chat,name='chat'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('moodTrack/',views.moodTracker,name='moodTrack'),
]
