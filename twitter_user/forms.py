from django import forms
from .models import TwitterUser
from django.contrib.auth.forms import UserCreationForm


class TwitterUserForm(UserCreationForm):
    class Meta:
        model = TwitterUser
        fields = "__all__"