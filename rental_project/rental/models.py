from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)
    responsible = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        
        if self.name:
            self.responsible = self.name.split()[0].lower()
        super().save(*args, **kwargs)


class Personnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username



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

class Part(models.Model):
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


    type = models.CharField( choices=PART_CHOICES)
    aircraft = models.CharField(choices=AIRCRAFT_CHOICES)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    is_assembled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.aircraft} {self.type}"
    
class Aircraft(models.Model):

    name = models.CharField(max_length=100, choices=AIRCRAFT_CHOICES)
    wing = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='wing', null=True)
    fuselage = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='fuselage', null=True)
    tail = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='tail', null=True)
    avionics = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='avionics', null=True)

    def __str__(self):
        return self.name
