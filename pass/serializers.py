from rest_framework import serializers
from .models import *
from base.serializers import addAttractionsSerializer

class cartedSpotSerializer(serializers.ModelSerializer):
    spots = addAttractionsSerializer(read_only = True , source = 'tourist_spots'  )
    
    class Meta:
        model= cartedSpots
        fields = ['id', 'tourist_spots', 'userPass', 'spots','members','start_date','end_date']




class passedSerializer(serializers.ModelSerializer):
    # cart = CartSerializer(read_only = True, source='userPass')
    items = cartedSpotSerializer(read_only = True, many=True)
    class Meta:
        model = passed
        fields = ['id','user','pass_code','items']
        read_only_fields = ['user']



  