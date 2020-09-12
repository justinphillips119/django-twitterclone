from django.db import models
from twitter_user.models import TwitterUser
from tweet_app.models import Tweet



class Notification(models.Model):
    tagged = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    tagged_tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
