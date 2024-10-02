from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    institution = models.CharField(max_length=255, blank=True)
    year_of_study = models.IntegerField(null=True, blank=True)
    mental_health_goal = models.TextField(blank=True)
    preferred_support = models.CharField(max_length=255, blank=True)
    favorite_movie_genre = models.CharField(max_length=255, blank=True)
    favorite_song_genre = models.CharField(max_length=255, blank=True)
    favorite_book_genre = models.CharField(max_length=255, blank=True)
    emergency_contact = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    current_emotional_state = models.CharField(max_length=255, blank=True)

    # Avoid clashes by defining unique related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Unique related_name for groups
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Unique related_name for user permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
