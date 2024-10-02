from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'age', 'institution', 'year_of_study',
                  'mental_health_goal', 'preferred_support', 'favorite_movie_genre', 'favorite_song_genre',
                  'favorite_book_genre', 'emergency_contact', 'emergency_contact_phone', 'current_emotional_state']
