from django.shortcuts import render, redirect, get_object_or_404
from .models import Personnel, Aircraft
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as authenticated_login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, PartForm
from .models import Part, AIRCRAFT_CHOICES
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView
from .serializers import PartSerializer, AircraftSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView



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
  
    form = PartForm()

    context = {
        'form': form,
    }
    return render(request, "rental/create-part.html", context)




@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login")
class PartListCreateAPIView(ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        # create a mutable copy
        data = request.data.copy()
        print(data)

        # Add the user's team to the created part model
        team = self.request.user.personnel.team
        data['team'] = team.pk  

   
        part_type = data.get('type')  # Get the part type from the request
        
        # Check if the user creating for their own team
        if part_type.lower() != team.responsible:
            return Response(
                {"detail": f"Your team is only responsible for creating parts of type '{team.responsible}'."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Pass the modified data to the serializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)  # Validate the data
        self.perform_create(serializer)  # Save the instance

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        
        aircraft_name = self.request.query_params.get('aircraft', None)
        if aircraft_name:
            # Fetch all parts for the aircraft
            return Part.objects.filter(aircraft=aircraft_name, is_assembled=False)
        team = self.request.user.personnel.team
        return Part.objects.filter(team=team)

    

class PartDetailAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # to ensure users only get parts belonging to their team
        team = self.request.user.personnel.team
        return Part.objects.filter(team=team)



@login_required(login_url="/login")
def assemble_aircraft(request):

  


    context = {
        "aircraft_choices": AIRCRAFT_CHOICES,
    }
    

    return render(request, "rental/assemble-aircraft.html", context)





class AircraftAPIView(APIView):
    def post(self, request):
        data = request.data
        print("Request data:", data)  # Debugging log
        aircraft_name = data.get("name")
        print("Aircraft name:", aircraft_name)



        wing = Part.objects.filter(type="Wing", aircraft=aircraft_name, is_assembled=False).first()
        fuselage = Part.objects.filter(type="Fuselage", aircraft=aircraft_name, is_assembled=False).first()
        tail = Part.objects.filter(type="Tail", aircraft=aircraft_name, is_assembled=False).first()
        avionics = Part.objects.filter(type="Avionics", aircraft=aircraft_name, is_assembled=False).first()

        print("Parts fetched:", wing, fuselage, tail, avionics)  # Debugging log

        if not wing or not fuselage or not tail or not avionics:
            return Response(
            {"detail": "One or more required parts are missing for this aircraft."},
            status=status.HTTP_400_BAD_REQUEST,)   
        
        wing.is_assembled = True
        fuselage.is_assembled = True
        tail.is_assembled = True
        avionics.is_assembled = True

        wing.save()
        fuselage.save()
        tail.save()
        avionics.save()

        created_aircraft = Aircraft.objects.create(
            name=aircraft_name,
            wing=wing,
            fuselage=fuselage,
            tail=tail,
            avionics=avionics
        )
        serializer = AircraftSerializer(created_aircraft)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self,request):

        created_aircrafts = Aircraft.objects.all()
        serializer = AircraftSerializer(created_aircrafts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

   

       
@login_required(login_url="/login")
def list_aircrafts(request):
    return render(request,"rental/list-aircraft.html")
