from django.db import models
from django.contrib.auth.models import User

# Create your models here.




TB2 = "TB2"
TB3 = "TB3"
AKINCI = "AKINCI"
KIZILELMA = "KIZILELMA"

AIRCRAFT_CHOICES = [
    (TB2, "TB2"),
    (TB3, "TB3"),
    (AKINCI,"AKINCI"),
    (KIZILELMA,"KIZILELMA")
]

WING = 'Wing'
FUSELAGE = 'Fuselage'
TAIL = 'Tail'
AVIONICS = 'Avionics'


PART_CHOICES = [
    (WING, 'Wing'),
    (FUSELAGE, 'Fuselage'),
    (TAIL, 'Tail'),
    (AVIONICS, 'Avionics'),
]

# One to many relation from team to personnel model

class Team(models.Model):
    name = models.CharField(max_length=100)
  
    def __str__(self):
        return self.name
    
class Personnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username
    
# one to many relation from aircraft to part models (its done by the use of foreign keys)
class Aircraft(models.Model):

    name = models.CharField(max_length=100, choices=AIRCRAFT_CHOICES)

    def __str__(self):
        return self.name

class Part(models.Model):
   
    type = models.CharField( choices=PART_CHOICES)
    aircraft_type = models.CharField(choices=AIRCRAFT_CHOICES)
    assembled_aircraft = models.ForeignKey(Aircraft, on_delete=models.PROTECT, null=True, blank=True)  # Tracks which aircraft the part is assigned to
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    is_assembled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.aircraft_type} {self.type}"
    