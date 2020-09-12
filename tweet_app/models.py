from django.db import models
from twitter_user.models import TwitterUser
from django.utils import timezone



class Tweet(models.Model):
    tweet = models.CharField(max_length=140)
    time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.tweet



