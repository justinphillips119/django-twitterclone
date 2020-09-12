from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from authentication_app.forms import RegistrationForm, LoginForm
from twitter_user.forms import TwitterUserForm
from twitter_user.models import TwitterUser


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = TwitterUser.objects.create_user(username=data.get("username"), password=data.get("password"), display_name=data.get("display_name"), bio=data.get("bio"))
            login(request, new_user)
            return HttpResponseRedirect(reverse("userfeed"))

    form = RegistrationForm()
    return render(request, "generic_form.html", {"form": form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, 
                username=data.get('username'), 
                password=data.get('password')
                )
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse('userfeed')))

    form = LoginForm()
    return render(request, 'generic_form.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))



