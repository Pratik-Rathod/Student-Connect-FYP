from . import views
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    re_path(r'^login_page/$',views.login_page,name='login'),
    path('register',views.register,name='register'),
    path('registerhandler/',views.registerhandler,name='registerhandler'),
    path('loginhandler/',views.loginhandler,name='loginhandler'),
    path('logouthandler/',views.logouthandler,name='logouthandler'),

    # path('sendemail/',views.send_mail, name ='sendmail'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('checkmail/',views.checkmail, name='checkmail'),  
    
    path('checkmail/',views.checkmail, name='checkmail'),  
    #path('accounts/', include('django.contrib.auth.urls')),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='authmaster/password/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='authmaster/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authmaster/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authmaster/password/password_reset_complete.html'), name='password_reset_complete'),      

]