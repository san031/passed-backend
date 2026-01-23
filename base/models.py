from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
import uuid
from django.conf import settings

# Create your models here.

# class User(AbstractUser):
#      name=models.CharField(max_length=255, blank=True, null=True)
#      email=models.EmailField(max_length=255,unique=True)
#      password=models.CharField(max_length=255)
#      username = None
     

#      USERNAME_FIELD = 'email'
#      REQUIRED_FIELDS = []

    #  def __str__(self):
    #       return self.username

class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100,default="")
     
# class Profile(models.Model):
#      user = models.OneToOneField(User,on_delete=models.CASCADE)
#      full_name=models.CharField(max_length=300)
#      def __str__(self):
#           return self.full_name


# def create_user_profile(sender, instance,created,**kwargs):
#      if created:
#           Profile.objects.create(user=instance)

# def save_user_profile(sender, instance, **kwargs):
#      instance.profile.save()

# post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile,sender=User)

class buyPass(models.Model):
    # name = models.CharField(max_length=40)
    # email = models.EmailField(max_length=254)
    class PassPlan(models.IntegerChoices):
        Day1=10, '1-Day Pass - $10'
        Day2 = 30 ,'3-Day Pass - $30'
        Day3 = 60,'6-Day Pass - $60'
    pass_type = models.IntegerField(choices=PassPlan.choices)
    pass_code = models.CharField(blank=True, max_length=8)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name= 'usePass')

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


# like category, city, ticket price, entry and exit point, title


class addAttractions(models.Model):
    class chooseCategory(models.TextChoices):
         library = 'LIBRARY','Library'
         historic_monument = 'HISTORIC MONUMENT','Historic Monument'
         meuseum = 'MEUSEUM','Meuseum'
         temple = 'TEMPLE','Temple'
         park = 'PARK','Park'
    my_id = models.AutoField(primary_key=True)
    category = models.CharField( max_length=20,choices=chooseCategory.choices, default='historic_monument', null=True)
    title=models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    is_featured=models.BooleanField(default=False)
    location = models.TextField(null=False, blank=False,default='')
    description = models.TextField(max_length=300, null=False,blank=False,default='')
    city= models.CharField(max_length=30,null=True)
    opening_time = models.TimeField(null=True)
    closing_time = models.TimeField(null=True)

    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    


    def __str__(self):
        return str(self.my_id)
    
def upload_path(instance, filename):
        return '/'.join(['spotImage', str(instance.spot.title), filename])

class spotImage(models.Model):
    spot = models.ForeignKey(addAttractions, on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(blank=True,null=True, upload_to=upload_path, max_length=500)

    def __str__(self):
        return str(self.spot.title)



class visitingData(models.Model):
     
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_Spot')
     start_date=models.DateField()
     end_date = models.DateField()
     members =models.IntegerField(default=1)
     visitingSpot = models.ForeignKey(addAttractions, on_delete=models.CASCADE,)

    
     def __str__(self):
        return str(self.user)
     
     def get_price(self):
         return self.visitingSpot.price





    


    
