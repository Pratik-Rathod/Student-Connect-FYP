from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import get_messages
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail as sm, BadHeaderError
from django.contrib.sites.shortcuts import get_current_site 

from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator

def checkmail(request):
    return render(request,'authmaster/checkmail.html')
   
def activate(request, uidb64, token):  
    User = get_user_model() 
    try:
        uid = force_str(urlsafe_base64_decode(uidb64)) 
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()    
        
        # lnuser =  authenticate(username=user.username,password=user.password)

        messages.success(request, "Email authentication successfull now you can login")
        return redirect('login')
        # userauth  = authenticate(username=str(user.username ),password = str( user.password ))
        # login(request,userauth)
    
    return HttpResponse('invild link')

# def send_mail(request):
#     res = sm(
#         subject = 'Subject here',
#         message = 'Here is the message.',
#         from_email = 'mail@gmail.com',
#         recipient_list = ['yymusic4@gmail.com'],
#         fail_silently=False,
#     )    

#     return HttpResponse(f"Email sent to {res} members")

# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')    
    return render(request,'authmaster/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')   
    return render(request,'authmaster/register.html')


def loginhandler(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
       
        loginuser = request.POST.get('usermame')
        loginpass = request.POST.get('password')
        
        userobj = User.objects.filter(username = loginuser).first()
      
        if userobj is None:
            messages.warning(request, "username or password wrong ")
            return redirect('login')
        
        cuser = authenticate(username=loginuser, password=loginpass)
        print(cuser)
        
        if not userobj.is_active:
                messages.warning(request, "email not verifed ")
                return redirect('login')
                
        if cuser is not None:
            

            
            login(request, cuser)
            return redirect('home')

        else:
            messages.warning(request, "Username or password wrong")
            return redirect('login')
    
    return HttpResponse("working log here bhago yaha se!")

def registerhandler(request):
    if request.method =='POST':
        userid = request.POST.get('userid')
        uemail = request.POST.get('email')
        upass = request.POST.get('password')
        upass2 = request.POST.get('cpassword')
        masscheck =  False
     
        if upass != upass2 :
            messages.warning(request, "Password did't match")
            masscheck = True    

        if User.objects.filter(username = userid).first() is not None:
            messages.warning(request, "Username already taken")
            masscheck = True

        if User.objects.filter(email = uemail).first() is not None:
            messages.warning(request, "Email already taken")
            masscheck = True

        if masscheck == True:
            masscheck = False
            return redirect('register')
       

        userdata = User.objects.create_user(username = userid,email=uemail,password = upass)
        userdata.is_active = False
        userdata.save()
     
        
        cursitedomain =  get_current_site(request)
        mail_subject = 'Activation link for student connect'

        message = render_to_string('acc_active_email.html', {  
                'user': userid,  
                'domain': cursitedomain.domain,  
                'uid':urlsafe_base64_encode(force_bytes(userdata.pk)),  
                'token':account_activation_token.make_token(userdata),  
             })  

        to_email = userdata.email
 
        res = sm(
                subject = mail_subject,
                message = message,
                from_email = 'studentconnecthelp1@gmail.com',
                recipient_list = [to_email],
                fail_silently=False,
          )
            
        if res>0: 
            return redirect('checkmail')

            # siteuser =  User.objects.create_user(username = userid,email=uemail,password = upass)
           
            # if siteuser is None:
            #     print("something went wrong")
            #     messages.success(request, "something went wrong")
            #     return redirect('register')
            
            # site_user = authenticate(username =userid , password  = upass)
                
            # if site_user is not None:
            #     login(request,site_user)
            #     return redirect('home') 
            # else:
            #     messages.success(request, "something went wrong please try agian later")
            #     print("something went wrong in while signup login")
            #     return redirect('register')
        # except:
            # print("something wrong")
            # return redirect('register')
    return HttpResponse("something went wrong from ourside please try again later")

@login_required(login_url='login')
def logouthandler(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "main/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						sm(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})