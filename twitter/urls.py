"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from tweet_app.views import homepage_view, user_feed_view, NewTweetView, profile_detail_view, TweetDetailView, FollowView, UnfollowView 
from authentication_app.views import register_view, login_view, logout_view
from notifications_app.views import NotificationView, NotificationCountView

urlpatterns = [
    path('', user_feed_view, name="userfeed"),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('homepage/', homepage_view, name="homepage"),
    path('newtweet/', NewTweetView.as_view(), name="newtweet"),
    path('profile/<str:username>/', profile_detail_view, name="profile"),
    path('tweet/<int:tweet_id>/', TweetDetailView.as_view(), name="tweet"),
    path('notifications/<int:user_id>/', NotificationView.as_view(), name="notifications"),
    path('follow/<str:username>/', FollowView.as_view(), name="follow"),
    path('unfollow/<str:username>/', UnfollowView.as_view(), name="unfollow"),
    path('admin/', admin.site.urls),
]
