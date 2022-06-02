from django.db import models
from django.contrib.auth.models import User 
from taggit.managers import TaggableManager

VOTE_CHOICES = (
    ("true", "true"),
    ("false", "false"),
    ("unset", "unset"),
)

# Create your models here.
class UserPost(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    cover_img =  models.ImageField(upload_to='img/',null=True,blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    lastupdate =  models.DateTimeField(editable=True,auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
  # tags = TaggableManager(help_text=None)


class UpVote(models.Model):
    post =  models.ForeignKey(UserPost,on_delete=models.CASCADE)
    user =  models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    response =  models.CharField(choices=VOTE_CHOICES,max_length=6,null=True)


class PostComments(models.Model):
    post =  models.ForeignKey(UserPost,on_delete=models.CASCADE)
    user =  models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    comment_body = models.TextField()   
    lastupdate =  models.DateTimeField(editable=True,auto_now_add=True)


# class PostComment(models.Model):    
#     post =  models.ForeignKey(UserPost,on_delete=models.CASCADE)
#     user =  models.ForeignKey(User,on_delete=models.CASCADE)
#     comment  = models.TextField()