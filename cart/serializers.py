from rest_framework import serializers
from .models import Cart, TourCartItem
from base.serializers import addAttractionsSerializer


class TourCartItemSerializer(serializers.ModelSerializer):
    spots = addAttractionsSerializer(read_only=True, source ='touristSpot')
    class Meta:
        model = TourCartItem
        fields = ['id','members','start_date','end_date','touristSpot','spots']
        read_only_fields = ['cart']
      

 
class CartSerializer(serializers.ModelSerializer):
    items = TourCartItemSerializer(many=True, read_only = True)

    
    class Meta:
        model = Cart
        fields = ['id','user','items']



    