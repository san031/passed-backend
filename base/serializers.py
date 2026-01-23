from rest_framework import serializers
from .models import buyPass,addAttractions,User, visitingData,spotImage
# from rest_framework.authentication import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']

        # extra_kwargs = {
        #     'password':{'write_only':True}                      #Set this to True to ensure that the field may be used when updating or creating an instance, 
        #                                                             #but is not included when serializing the representation.
        # }

          # Hash the password before saving     
    def validate_password(self, value):
        return make_password(value)
    

    # def create(self,validated_data):
    #     password = validated_data.pop('password',None)
    #     instance = self.Meta.model(**validated_data)  #doesnot include password

    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance

# class NewTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token=super().get_token(user)    
    #     token['full_name'] = user.profile.fullname
    #     token['username']  =user.username
    #     token['email'] = user.email

# class RegisterSerializer(serializers.ModelSerializer):
#     password=serializers.CharField(
#         write_only = True,
#         required=True,
#         validators= [validate_password]
#     )

#     password2=serializers.CharField(
#         write_only = True,
#         required=True,
#     )

#     class Meta:
#         model=User
#         fields=['email','username','password','password2']

#         def validate(self,attrs):
#             if attrs['password']!=attrs['password2']:
#                 raise serializers.ValidationError(
#                     {"password":"Passwords fields do not match"}
#                 )
            
#             return attrs
        
#         def create(self,validated_data):
#             user = User.objects.create(
#                 username= validated_data['username'],
#                 email = validated_data['email']
#             )
#             user.set_password(validated_data['password'])
#             user.save()
#             return user

class BuyPassSerializer(serializers.ModelSerializer):
    class Meta:
        model=buyPass
        # fields = ('id','pass_type','pass_code','user')
        fields = '__all__'

class ImageSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = spotImage
        fields = '__all__'


class addAttractionsSerializer(serializers.ModelSerializer):
    images = ImageSpotSerializer(read_only = True, many = True)

    uploaded_images = serializers.ListField(
        # child = serializers.ImageField(max_length = 100,allow_empty_file = False, use_url = False)
        child = serializers.ImageField(allow_empty_file = False),
        write_only = True
    )
    
    class Meta:
        model = addAttractions
        fields = ('my_id','category','title','price','is_featured','location',
                  'description','city','opening_time','closing_time','uploaded_images','images')
        
    def create(self, validated_data):
        uploaded_data = validated_data.pop('uploaded_images')
        new_spot = addAttractions.objects.create(**validated_data)
        for upload_item in uploaded_data:
            spotImage.objects.create(spot = new_spot,image = upload_item)
        return new_spot

class visitingDataSerializer(serializers.ModelSerializer):
    # tourist_Spot = addAttractionsSerializer( read_only=True)
    visitingSpot = addAttractionsSerializer(read_only = True)
    
    class Meta:
        model = visitingData
        fields = ['user','start_date','end_date','members','visitingSpot']

        def validate(self,value):
            start_date = value.get('start_date')
            end_date  = value.get('end_date')
            if end_date<start_date:
                raise serializers.ValidationError("End date must be greater than start date")
            
            return value
        
    


# class loginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('name','email','password','username')

class ProfileSerializer(UserSerializer,BuyPassSerializer):
    class Meta(UserSerializer.Meta,BuyPassSerializer.Meta):
        fields = [UserSerializer.Meta.fields, BuyPassSerializer.Meta.fields]


class UserRegisterTokenSerializer(UserSerializer):
    token=serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = User
        fields =  ["id","username","email","token"]

    def get_token(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    

# class CustomTOkenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.username
#         return token
    
#     def validate(self, attrs):
#         try:
#             data = super().validate(attrs)
#             user_data = UserRegisterTokenSerializer(self.user).data
#             data.update(user_data)
#             data['user'] = self.user
#             return data
#         except AuthenticationFailed:
#             return ("Invalid credentials, please try again.")
#         except User.DoesNotExist:
#             return "User Does Not exist"
        
#         except Exception as e:
#             return "An error occured during authentication"