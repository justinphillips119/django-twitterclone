from django.shortcuts import render, reverse, HttpResponseRedirect
from twitter_user.models import TwitterUser
from tweet_app.models import Tweet
from notifications_app.models import Notification
from django.contrib.auth.decorators import login_required



@login_required
def notification_view(request, user_id):
    tweets = Notification.objects.filter(tagged=request.user)
    count = 0
    notification_list = []
    for tweet in tweets:
        if tweet.read == False:
            count += 1
            notification_list.append(tweet.tagged_tweet)
            tweet.read = True
            tweet.save()
    return render(request, "notifications.html", {"tagged": notification_list, "count": count})



def notification_count_view(request):
    user = request.user
    if user.is_authenticated:
        notifications = Notification.objects.filter(tagged=user)
        count = 0
        for notification in notifications:
            if notification.read == False:
                count += 1
    else:
        count = 0
    return count



