from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from base.models import addAttractions
from rest_framework import serializers

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name= 'userCart', null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.user)


class TourCartItem(models.Model):

    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='items', null=True)
    touristSpot = models.ForeignKey(addAttractions,on_delete=models.CASCADE, related_name='spot')
    start_date=models.DateField()
    end_date = models.DateField()
    members =models.IntegerField(default=1)

    # def validate_date(self,value):
    #     if value.start_date>value.end_date:
    #         raise serializers.ValidationError("Start date must be less than end date")
        
    #     return value

    
    class Meta:
        unique_together = ('cart', 'touristSpot')

    def save(self, *args, **kwargs):
        if TourCartItem.objects.filter(cart=self.cart, touristSpot= self.touristSpot).exists() and not self.pk:
            raise serializers.ValidationError("The product already exists")
        
        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.touristSpot.title)