from django.contrib import admin
from .models import *
from base.models import User
# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     list_display=['username','email']

# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user','full_name']

class PassAdmin(admin.ModelAdmin):
    list_display = ['get_email','get_user']

    def get_email(self, value):
        if value.user.email:
            return value.user.email
        

        return "No email spotted"
    
    def get_user(self,value):
        if value.user.username:
            return value.user.username
        
        return "No username entered"
    
admin.site.register(buyPass,PassAdmin)

admin.site.register(User)
# admin.site.register(PassAdmin)
# admin.site.register(buyPass)
admin.site.register(addAttractions)
admin.site.register(visitingData)
admin.site.register(spotImage)
