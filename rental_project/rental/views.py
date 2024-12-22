from django.shortcuts import render, redirect, get_object_or_404
from .models import Personnel, Aircraft, Team
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as authenticated_login, logout
from django.contrib.auth.decorators import login_required

from .models import Part, AIRCRAFT_CHOICES, Team, PART_CHOICES
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView
from .serializers import PartSerializer, AircraftSerializer, TeamSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView



# Create your views here.


########### LOGIN SCREEN VIEWS

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        team_id = request.POST.get('team')

        if username and password and team_id:
            # Create the user
            user = User.objects.create_user(username=username, password=password)
            
            # Fetch the team object based on team_id
            team = Team.objects.get(pk=team_id)

            # create the personnel with user and team fields added
            Personnel.objects.create(user=user, team=team)

           
            

            messages.success(request, "Your account has been created successfully.")
            return redirect('login')  
        else:
            messages.error(request, "Please fill all fields correctly.")

    return render(request, "rental/register.html")




def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            authenticated_login(request, user)
            
            return redirect('index') 
        else:
           
            messages.error(request, "Invalid username or password")

    
    return render(request, "rental/login.html")

########### MAIN SCREENS

@login_required(login_url="/login")
def index(request):

    
    context = {'user': request.user}
    return HttpResponseRedirect("/create-parts")



@login_required(login_url="/login")
def create_parts(request):
  
    return render(request, "rental/create-part.html")




@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login")
class PartListCreateAPIView(ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        # create a mutable copy (because we are going to set the team field)
        data = request.data.copy()
      
        # add the user's team to the created part model
        team = self.request.user.personnel.team
        data['team'] = team.pk  
        
        # a variable which contains the team responsibility e.g. "wing" , "avionics"
        team_responsibility = team.name.split()[0].lower()
   
        part_type = data.get('type') 
        part_names = PART_CHOICES

        # get the teams responsible for parts
        current_teams = []
        for tuple in part_names:
            for part in tuple:
                current_teams.append(part.lower())
        
        # check if the user creating for their own team
        if part_type.lower() !=  team_responsibility:

            if team_responsibility not in current_teams: # then its assembly team
                detail ="Your team is only responsible for Assembly."
            else: # then its part creation team but wrong type
                detail = f"Your team is only responsible for creating parts of type '{ team_responsibility }'."

            return Response( 
                {"detail": detail},
                status=status.HTTP_403_FORBIDDEN,
            )

       
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)  
        self.perform_create(serializer)  # save the validated data as a db instance

       
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
     
        queryset = Part.objects.all()
        
        aircraft = self.request.query_params.get('aircraft', None)
        
        

        assembled_aircraft = self.request.query_params.get('assembled_aircraft', None)
        
        # if there is an assembled aircraft param return the corresponding parts ( for list aircraft page)
        if  assembled_aircraft:
            queryset = queryset.filter(assembled_aircraft_id=assembled_aircraft)
            print(queryset)
            return queryset
        
        # if there is an  aircraft param return the associated parts ( for checking available parts)
        elif  aircraft:
            queryset = queryset.filter(assembled_aircraft=None,aircraft_type=aircraft)
            return queryset
        
        # if there is no param just return parts for the corresponding team
        team = self.request.user.personnel.team
        return Part.objects.filter(team=team, is_assembled=False)

    

class PartDetailAPIView(RetrieveUpdateDestroyAPIView):
    

    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated]


    # to ensure users can only delete parts belonging to their team
    def get_queryset(self):
        team = self.request.user.personnel.team
        return Part.objects.filter(team=team)




@login_required(login_url="/login")
def assemble_aircraft(request):

    # pass aircraft choices as a context to the assemble page
    context = {
        "aircraft_choices": AIRCRAFT_CHOICES,
    }
    

    return render(request, "rental/assemble-aircraft.html", context)




# AircraftAPI to assemble aircrafts
class AircraftAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):

        team = request.user.personnel.team
        team_name = team.name.split()[0]
        
        print("------")
        if team_name.lower() != "assembly":
            return Response(
                {"detail": "Your team is not authorized to assemble aircraft."},
                status= status.HTTP_403_FORBIDDEN
            )
    
        data = request.data
     

        # fetch the counts from the post data
        aircraft_name = data.get("name")
        wing_count = int(data.get("wing_count", 0))
        fuselage_count = int(data.get("fuselage_count", 0))
        tail_count = int(data.get("tail_count", 0))
        avionics_count = int(data.get("avionics_count", 0))

        # filter the suitable parts for that specific aircraft based on the number of parts needed
        wings = Part.objects.filter(type="Wing", aircraft_type=aircraft_name, is_assembled=False)[:wing_count]
        fuselages = Part.objects.filter(type="Fuselage", aircraft_type=aircraft_name, is_assembled=False)[:fuselage_count]
        tails = Part.objects.filter(type="Tail", aircraft_type=aircraft_name, is_assembled=False)[:tail_count]
        avionics = Part.objects.filter(type="Avionics", aircraft_type=aircraft_name, is_assembled=False)[:avionics_count]


        missing_parts = []
        if len(wings) < wing_count:
            missing_parts.append(f"Wings: {wing_count - len(wings)} part is missing.")
        if len(fuselages) < fuselage_count:
            missing_parts.append(f"Fuselages: {fuselage_count - len(fuselages)} part is missing.")
        if len(tails) < tail_count:
            missing_parts.append(f"Tails: {tail_count - len(tails)} part is missing.")
        if len(avionics) < avionics_count:
            missing_parts.append(f"Avionics: {avionics_count - len(avionics)} part is missing.")

        # Return error message if any parts are missing
        if missing_parts:
            return Response(
                {   "missing_parts": missing_parts},
                    status=status.HTTP_400_BAD_REQUEST,
            )
        

        created_aircraft = Aircraft.objects.create(name=aircraft_name)

        # assign parts to the aircraft and mark them as assembled
        part_list = [*wings, *fuselages, *tails, *avionics]
        for part in part_list:
            part.is_assembled = True
            part.assembled_aircraft = created_aircraft  # assign the aircraft to each part used
            part.save()  
           

        
        
        serializer = AircraftSerializer(created_aircraft)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self,request):

        created_aircrafts = Aircraft.objects.all()
        serializer = AircraftSerializer(created_aircrafts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

   

       
@login_required(login_url="/login")
def list_aircrafts(request):

    team = request.user.personnel.team

    team_name = team.name.split()[0].lower()


    if( team_name != "assembly"):
       messages.warning(request, "You are not an assembly team member.")
       return  HttpResponseRedirect("/create-parts")
    

    return render(request,"rental/list-aircraft.html")


class TeamListAPIView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    