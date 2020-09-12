from django.shortcuts import render, reverse, HttpResponseRedirect
from twitter_user.models import TwitterUser
from tweet_app.models import Tweet
from tweet_app.forms import TweetForm
from notifications_app.models import Notification
from notifications_app.views import notification_view, notification_count_view
from django.contrib.auth.decorators import login_required
import re



def homepage_view(request):
    return render(request, "index.html")



@login_required
def user_feed_view(request):
    user = Tweet.objects.filter(user=request.user)
    following = Tweet.objects.filter(user__in=request.user.following.all())
    notifications = notification_count_view(request)
    feed = user | following
    feed = feed.order_by("-time")
    return render(request, "userfeed.html", {"feed": feed, "notifications": notifications})



@login_required
def new_tweet_view(request):
    notifications = notification_count_view(request)
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

    form = TweetForm()
    return render(request, "generic_form.html", {"form": form})



def profile_detail_view(request, username):
    user = TwitterUser.objects.filter(username=username).first()
    tweets = Tweet.objects.filter(user=user).order_by("-time")
    tweet_count = len(Tweet.objects.filter(user=user).all())
    notifications = notification_count_view(request)
    following_count = len(user.following.all())
    if request.user.is_authenticated:
        following = request.user.following.all()
    else:
        following = []
    return render(request, "profile.html", {"user": user, "tweets": tweets, "notifications": notifications, "following": following, "tweet_count": tweet_count, "following_count": following_count})



def tweet_detail_view(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    return render(request, "tweet.html", {"tweet": tweet})



def follow_view(request, username):
    user = request.user
    follow_user = TwitterUser.objects.filter(username=username).first()
    user.following.add(follow_user)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



def unfollow_view(request, username):
    user = request.user
    unfollow_user = TwitterUser.objects.filter(username=username).first()
    user.following.remove(unfollow_user)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

