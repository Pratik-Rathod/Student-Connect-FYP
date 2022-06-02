from email.quoprimime import body_check
from http.client import FORBIDDEN
import json
from multiprocessing import context
from turtle import pos
from urllib import request
from django.contrib import messages
from sre_constants import SUCCESS
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import UserPost
from .models import UpVote
from . import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import UserPostForm
from profile_master.models import followUser
from profile_master.models import UserPrefInfo
# Create your views here.


def followed_view(request):
    followed_users =  followUser.objects.values_list('following_user_id',flat=True).filter(user_id=request.user)
    post_objs = UserPost.objects.filter(author__in =set(followed_users)).order_by("-lastupdate")
    followedUserInfo = UserPrefInfo.objects.filter(User__in =set(followed_users))
    followedusercount = UserPrefInfo.objects.filter(User__in =set(followed_users)).count()
    
    thisdict  = {}
    
    for userPos in post_objs:
        try:
            vote = UpVote.objects.get(user=request.user,post=userPos)
            if vote:
                thisdict[userPos] = vote
        except:
            pass    

    context ={
        'post_obj':post_objs,
        'upvotelist':thisdict,
        'followedUserInfo':followedUserInfo,
        'followedusercount':followedusercount
    }
    
    return render(request,'home/followedpaged.html',context)

def test(request):    
    context ={
    'form':UserPostForm()
    }
    return render(request,'home/test.html',context)

@login_required(login_url='/login_page/')
def post(request):
    if request.method=='POST':
        try:
            form =  UserPostForm(request.POST,request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.author = request.user
                obj.save()
                messages.success(request, " post successfully added ")
        except:
            messages.warning(request, " Developer did something wrong ")
        
        return redirect('home')
    return HttpResponse("402 invvilid header")

def search_view(request):
    if request.method =='GET':
        q = request.GET.get('q')
        search_items = UserPost.objects.filter(Q(title__contains=q) |Q(body__contains=q)).order_by('-lastupdate') 
        context = {'q':q,'post_objs':search_items}
        return render(request,'home/search.html',context)
        
def home(request):

    post_objs = UserPost.objects.filter().order_by("-lastupdate")
    postform = UserPostForm()
    # checked = None
    # if request.user.is_authenticated:
    #     checked  =  models.UpVote.objects.filter(user=request.user).exclude(response='unset')
    # d  context.add('checked',checked)
    thisdict  = {}
    for userPos in post_objs:
        try:
            vote = UpVote.objects.get(user=request.user,post=userPos)
            if vote:
                thisdict[userPos] = vote
        except:
            pass  
    context = {'post_objs':post_objs,'postform':postform,'upvotelist':thisdict}
          
    return render(request,'home/index.html',context)

def mypost(request):
    return render(request,'home/index.html')

@login_required(login_url='/login_page/')
def vote(request):
    print("success")
      
    if request.method == 'GET':
        post_id = request.GET['post_id']
        resp = request.GET.get('res')
        user_liked_post  = UserPost.objects.get(pk=post_id)
        cur_user = request.user
        try:
            if resp == "unset":
                models.UpVote.objects.filter(post=user_liked_post,user=cur_user).delete()
                return HttpResponse("success")     
        except:
             return HttpResponse("something went wrong here ")

        models.UpVote.objects.update_or_create(post=user_liked_post,user=cur_user)
        
        modelobj = models.UpVote.objects.get(post=user_liked_post,user=cur_user)
        modelobj.user = cur_user
        modelobj.response = resp
        modelobj.save()
        return HttpResponse("success")

    else:
       return HttpResponse("Something went wrong")

def img(request):
    return HttpResponse(SUCCESS)

@login_required(login_url='/login_page/')
def comments(request,pk):
    try:
        postobj= UserPost.objects.get(pk=pk)
        notes = models.PostComments.objects.filter(post=pk).order_by('-lastupdate')
        context = {'post':postobj,'notes':notes}
    except:
        messages.success(request, " post successfully added ")

    return render(request,'home/comment_page.html',context)

@login_required(login_url='/login_page/')
def addnote(request):
    try:
        if request.method == 'POST':
            json_data = json.loads(request.POST.get("form"))
            postid = json_data[1]['value']
            note = json_data[2]['value'] 
            models.PostComments.objects.create(post=models.UserPost.objects.get(pk=postid),user=request.user,comment_body=note)
    except:
        print("internal work")
    return HttpResponse(SUCCESS)