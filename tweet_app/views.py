from django.shortcuts import render, reverse, HttpResponseRedirect
from twitter_user.models import TwitterUser
from tweet_app.models import Tweet
from tweet_app.forms import TweetForm
from notifications_app.models import Notification
from notifications_app.views import NotificationView, NotificationCountView
from django.contrib.auth.decorators import login_required
import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView



def homepage_view(request):
    return render(request, "index.html")



@login_required
def user_feed_view(request):
    user = Tweet.objects.filter(user=request.user)
    following = Tweet.objects.filter(user__in=request.user.following.all())
    notifications = NotificationCountView.as_view()
    feed = user | following
    feed = feed.order_by("-time")
    return render(request, "userfeed.html", {"feed": feed, "notifications": notifications})



class NewTweetView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        notifications = NotificationCountView.as_view()
        form = TweetForm()
        return render(request, "generic_form.html", {"form": form})

    def post(self,request):
        notifications = NotificationCountView.as_view()
        if request.method == 'POST':
            form = TweetForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                post = Tweet.objects.create(
                    tweet=data.get('tweet'),
                    user=request.user,
                )
                tags = re.findall(r'@(\w+)', data.get('tweet'))
                if tags:
                    for tag in tags:
                        tagged_user = TwitterUser.objects.get(username=tag)
                        if tagged_user:
                            Notification.objects.create(
                                tagged=tagged_user,
                                tagged_tweet=post
                            )
                return HttpResponseRedirect(reverse("userfeed"), {"notifications": notifications})



def profile_detail_view(request, username):
    user = TwitterUser.objects.filter(username=username).first()
    tweets = Tweet.objects.filter(user=user).order_by("-time")
    tweet_count = len(Tweet.objects.filter(user=user).all())
    notifications = NotificationCountView.as_view()
    following_count = len(user.following.all())
    if request.user.is_authenticated:
        following = request.user.following.all()
    else:
        following = []
    return render(request, "profile.html", {"user": user, "tweets": tweets, "notifications": notifications, "following": following, "tweet_count": tweet_count, "following_count": following_count})



class TweetDetailView(TemplateView):
    def get(self, request, tweet_id):
        tweet = Tweet.objects.get(id=tweet_id)
        return render(request, "tweet.html", {"tweet": tweet})



class FollowView(TemplateView):
    def get(self, request, username):
        user = request.user
        follow_user = TwitterUser.objects.filter(username=username).first()
        user.following.add(follow_user)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



class UnfollowView(TemplateView):
    def get(self, request, username):
        user = request.user
        unfollow_user = TwitterUser.objects.filter(username=username).first()
        user.following.remove(unfollow_user)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
