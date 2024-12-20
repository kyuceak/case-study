from rest_framework import serializers
from .models import Part, Aircraft



class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'

 

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'