from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Team, Personnel
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as authenticated_login


# Create your views here.



def index(request):
    context = {}
    return render(request, "rental/index.html")


# extending UserCreationForm to add team dropdown field
class register_form(forms.ModelForm):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'team')


def register(request):
    if request.method == 'POST':
        form = register_form(request.POST)
        if form.is_valid():
            # Create the user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            # Associate the user with a team
            team = form.cleaned_data.get('team')
            Personnel.objects.create(user=user, team=team)

            # Log in the user
            messages.success(request, "Your account has been created. Please log in.")
            return HttpResponseRedirect("/login")
    else:
        form = register_form()

    context = {'form': form}
    return render(request, "rental/register.html", context)

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )


def login(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                authenticated_login(request,user)
                return HttpResponseRedirect("")
            else:
                messages.error(request, "Invalid username or password")

    else:
        form = LoginForm()

    context = {'form':form}
    return render(request, "rental/login.html", context)

