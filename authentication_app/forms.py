from django import forms
from twitter_user.models import TwitterUser


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=80)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = TwitterUser
        fields = ["display_name", "bio"]



class LoginForm(forms.Form):
    username = forms.CharField(max_length=80, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


