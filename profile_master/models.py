from pyexpat import model
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserPrefInfo(models.Model):
    User = models.OneToOneField(User,on_delete=models.CASCADE)
    coverImg = models.URLField(default='https://picsum.photos/seed/lol/1200/200')
    avtarImg = models.URLField(default='https://avatars.dicebear.com/api/pixel-art/asd.svg')

class followUser(models.Model):
    user_id = models.ForeignKey(User, related_name="following",on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers",on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
