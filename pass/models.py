from django.db import models
import uuid
from cart.models import Cart
from django.conf import settings
from base.models import addAttractions
from datetime import date


class passed(models.Model):
    # name = models.CharField(max_length=40)
    # email = models.EmailField(max_length=254)
    # class PassPlan(models.IntegerChoices):
    #     Day1=10, '1-Day Pass - $10'
    #     Day2 = 30 ,'3-Day Pass - $30'
    #     Day3 = 60,'6-Day Pass - $60'
    # pass_type = models.IntegerField(choices=PassPlan.choices)
    pass_code = models.CharField(blank=True, max_length=8)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    # total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # userPass = models.OneToOneField(Cart, on_delete=models.CASCADE,related_name= 'usePass')
    # cart_spots = models.ForeignKey(cartedSpots, on_delete=models.CASCADE, related_name='spots_cart', null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
    
    def save(self, *args, **kwargs):
        if not self.pass_code:
            self.pass_code = str(uuid.uuid4()).replace("-","").upper()[:8] 
        super().save(*args, **kwargs)

    def get_email(self, value):
        if value.user.email:
            return value.user.email
        

        return "No email spotted"
    
class cartedSpots(models.Model):
    members = models.IntegerField(default=1)
    start_date=models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    tourist_spots = models.ForeignKey(addAttractions, on_delete=models.CASCADE)
    userPass = models.ForeignKey(passed, related_name='items', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.tourist_spots.title