import json
from multiprocessing import context
from sre_constants import SUCCESS
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import UserPrefInfo
from django.contrib import messages
from home.models import UserPost
from django.contrib.auth.models import  User
from home.models import UpVote
from . import models
# Create your views here.

@login_required(login_url='/login_page/')
def deletepost_view(request,pk):
    try:
        UserPost.objects.filter(pk=pk,author = request.user).delete()
        messages.success(request,"deleted successfully")
    except:
        messages.success(request,"internal server had heart attack try again later")

    return redirect('profile')
    
@login_required(login_url='/login_page/')
def profile_view(request):
    context = None 
    try:
        pref = UserPrefInfo.objects.get(User=request.user)
        userPost = UserPost.objects.filter(author= request.user).order_by('-lastupdate')  
       # UpVote.objects.filter(user=request.user).order_by('userPost__lastupdate')
        thisdict  = {}


        for userPos in userPost:
            try:
                vote = UpVote.objects.get(user=request.user,post=userPos)
                if vote:
                    thisdict[userPos] = vote
            except:
                pass    
        post = UserPost.objects.filter(author = request.user) 
    

        count = UpVote.objects.filter(post__in=post,response='true').count()
       # votes = UpVote.objects.filter(user=request.user).order_by('userPost__lastupdate')
        
        context = {
            'pref':pref,
            'userPost':userPost,
            'upvotes':count,
            'upvotelist':thisdict
        }
        
    except Exception as e:
        print(e)
    return render(request,'profile_master/authorprofile.html',context)

@login_required(login_url='/login_page/')
def user_view(request,pk):
    context = None 
    try:
        if User.objects.get(pk=pk) == request.user:
            return redirect('profile')
        usr = User.objects.get(pk=pk)
        print(type(usr))
        pref = UserPrefInfo.objects.get(User=usr)
        userPost = UserPost.objects.filter(author= usr).order_by('-lastupdate')  
        post = UserPost.objects.filter(author = usr) 
        print(post)
        count = UpVote.objects.filter(post__in=post,response='true').count()
        print(count)
       
       #get User likes
        thisdict  = {}
        for userPos in userPost:
            try:
                vote = UpVote.objects.get(user=request.user,post=userPos)
                if vote:
                    thisdict[userPos] = vote
            except:
                pass  
        
        # upvotes = UpVote.objects.filter(response='true').filter(post = UserPost.objects.filter(author = usr)).count()
        isfollowed = models.followUser.objects.filter(user_id=request.user,following_user_id=User.objects.get(pk=pk)).exists()
       
        context = {
            'pref':pref,
            'userPost':userPost,
            'upvotes':count,
            'isfollowed':isfollowed,
            'upvotelist':thisdict
        }
    except Exception as e:
        print(e)
    return render(request,'profile_master/userprofile.html',context)

def save_profile_img(request):
    if request.method =='POST':
        try:
            json_data =json.loads(request.POST.get("imgdata"))
            UserPrefInfo.objects.update_or_create(
                User = request.user
            )
            modelObj =  UserPrefInfo.objects.get(User =request.user)
            modelObj.coverImg = json_data['coverimg']
            modelObj.avtarImg = json_data['useravtar']
            modelObj.save()
        except:
            return HttpResponse("something went wrong")
    return HttpResponse(SUCCESS)

def follow(request):
    if request.method == 'GET':
        userid =  request.GET.get('userid')
        exist = models.followUser.objects.filter(user_id=request.user,following_user_id=User.objects.get(pk=userid)).exists()
        if exist:
            print('deleted!')
            models.followUser.objects.filter(user_id=request.user,following_user_id=User.objects.get(pk=userid)).delete()
        else:
            print('created!')
            models.followUser.objects.create(user_id=request.user,following_user_id=User.objects.get(pk=userid))

    return HttpResponse('working')