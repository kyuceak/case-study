from django.shortcuts import render, redirect, get_object_or_404
from .models import Personnel
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as authenticated_login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, PartForm
from .models import Part
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Part
from .serializers import PartSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status



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
 
    return render(request, "rental/create-part.html")




           


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

class PartListCreateAPIView(ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        # Create a mutable copy of the request data
        data = request.data.copy()

        # Add the user's team to the data
        team = self.request.user.personnel.team
        data['team'] = team.pk  # Use the team's ID since it's a ForeignKey

        # Check if the part type matches the team's responsibility
        part_type = data.get('type')  
        print(part_type)
        print("----")
        print(team.responsible)
        if part_type.lower() != team.responsible:
            return Response(
                {"detail": f"Your team is only responsible for creating parts of type '{team.responsible}'."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Pass the modified data to the serializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True) 
        self.perform_create(serializer)  

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        # Only return parts for the logged-in user's team
        team = self.request.user.personnel.team
        return Part.objects.filter(team=team)

    

class PartDetailAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Ensure users can only retrieve or modify parts belonging to their team
        team = self.request.user.personnel.team
        return Part.objects.filter(team=team)
    