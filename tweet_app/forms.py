from django import forms
from tweet_app.models import Tweet


class TweetForm(forms.ModelForm):
    tweet = forms.CharField(widget=forms.Textarea, max_length=140)

    class Meta:
        model = Tweet
        fields = ['tweet']
        exclude = ['time', 'user']