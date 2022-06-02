from django.conf import settings
from . import views
from django.urls import path,re_path
from django.conf.urls.static import static

urlpatterns = [
    path('user/<int:pk>',views.user_view,name='user'),
    path('profile',views.profile_view,name='profile'),
    path('follow',views.follow,name='follow'),
    path('saveprofileimgs',views.save_profile_img,name='saveprofileimgs'),
    path('deletepost/<int:pk>',views.deletepost_view,name='deletepost'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)