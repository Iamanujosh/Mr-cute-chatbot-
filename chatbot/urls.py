from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('chat/',views.chat,name='chat'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login_view,name='login'),
   path('home/',views.home,name='home'),
]

