from django.db import models
from django.contrib.auth.models import AbstractUser


class TwitterUser(AbstractUser):
    display_name = models.CharField(max_length=80)
    bio = models.TextField(null=True, blank=True)
    following = models.ManyToManyField("self", symmetrical=False)

    def __str__(self):
        return self.username


