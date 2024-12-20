from django.shortcuts import render, redirect
from .models import Personnel
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as authenticated_login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm


# Create your views here.


########### LOGIN SCREEN VIEWS

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
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
            print(form.errors)
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, "rental/register.html", context)




def login(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                authenticated_login(request,user)
                return index(request) # open main page after login
            else:
                messages.error(request, "Invalid username or password")

    else:
        form = LoginForm()

    context = {'form':form}
    return render(request, "rental/login.html", context)

########### MAIN SCREENS

@login_required(login_url="/login")
def index(request):

    
    context = {'user': request.user}
    return render(request, "rental/index.html", context)



@login_required(login_url="/login")
def create_parts(request):
    pass

@login_required(login_url="/login")
def list_parts(request):
    pass

@login_required(login_url="/login")
def create_aircrafts(request):
    pass

@login_required(login_url="/login")
def list_aircrafts(request):
    pass

@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login")