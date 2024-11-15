"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backend.views import UserRegisterView,LoginView,CreatePostView,ListPostView,UnPublishPostView,PostLikeView,PostUnLikeView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/register/',UserRegisterView.as_view() ,name='register'),
    path('user/login/',LoginView.as_view() ,name='login'),
    path('user/post/',CreatePostView.as_view() ,name='post'),
    path('user/unpost/',UnPublishPostView.as_view() ,name='unpost'),
    path('post/list/',ListPostView.as_view() ,name='post-list'),    
    path('post/like/',PostLikeView.as_view() ,name='like'),
    path('post/unlike/',PostUnLikeView.as_view() ,name='unlike'),
]

#   http://127.0.0.1:8000/user/register/   for registering user
#   http://127.0.0.1:8000/user/login/      for login user
#   http://127.0.0.1:8000/user/post/       for Publising a post
#   http://127.0.0.1:8000/user/unpost/     for unpublishing a post
#   http://127.0.0.1:8000/post/list/       for listing the posts
#   http://127.0.0.1:8000/post/like/       for liking the post
#   http://127.0.0.1:8000/post/unlike/     for unliking the post



