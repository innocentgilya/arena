from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    ''' extends the user definition '''
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    profiles = models.ManyToManyField('Profile', blank=True, related_name='profile')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    '''a class that defines a user profile'''
    #id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profiles')
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True, default=timezone.now)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    school = models.CharField(max_length=50)
    grade = models.CharField(max_length=50)


    def __str__(self):
        return self.name



