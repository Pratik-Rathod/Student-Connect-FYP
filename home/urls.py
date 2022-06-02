from django.urls import include, path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('mypost', views.mypost, name='mypost'),
    path('',views.home,name='home'),
    path('post/<int:pk>/comments',views.comments,name='comments'),
    path('addnote/',views.addnote,name='addnote'),
    path('post',views.post,name='post'),
    path('search/',views.search_view,name='search'),
    path('followed',views.followed_view,name='followed'),
    path('media/',views.img,name='media'),
    # path('test',views.test,name='test'),
    re_path(r'^vote/$', views.vote, name='vote'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)