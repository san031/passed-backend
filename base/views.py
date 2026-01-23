from rest_framework import viewsets,permissions
from .serializers import *
from .models import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from base.filters import SpotFilter
from django_filters.rest_framework import DjangoFilterBackend



# Create your views here.


class BuyPassViewSet(viewsets.ViewSet):
    permission_classes=[permissions.AllowAny]
    query_set=buyPass.objects.all()
    serializer_class=BuyPassSerializer

    def list(self,request):
        query_set=self.query_set
        serializer=self.serializer_class(query_set, many=True)
        return Response(serializer.data)

    def post(self,request):
        self.permission_classes = [permissions.IsAuthenticated]
        serializer=BuyPassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


        
class AddAttractionsViewSet(viewsets.ViewSet):
    permission_classes=[permissions.AllowAny]
    query_set = addAttractions.objects.all()
    serializer_class= addAttractionsSerializer
    

    def get_queryset(self):
        query_set = self.query_set
        qs=self.request.GET.get('title')

        if qs:
            query_set = query_set.filter(title__icontains = qs)
            return query_set
        
        else:
            return self.query_set
        

        

    def featuredSpots(self,request):
        queryset = addAttractions.objects.filter(is_featured = True)
        serializer = self.serializer_class(queryset, many = True)
        return Response(serializer.data)


    def list(self,request):
        query_set = self.get_queryset()
        serializer = self.serializer_class(query_set,many = True)
        # filter_backends = [DjangoFilterBackend]
        # filterset_class = SpotFilter
        filterset_fields = ('title','category','location')
        print(query_set)
        return Response(serializer.data)

    
    
    def retrieve_spot(self,request,pk=None):
        tourist_spot = addAttractions.objects.get(my_id = pk)
        serializer = self.serializer_class(tourist_spot)
        return Response(serializer.data)
    
    def partial_update(self, request, pk=None):
        id=pk
        query_set = get_object_or_404(addAttractions, pk=pk)

        serializer = addAttractionsSerializer(query_set,data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Partial Data Updated"})
        return Response(serializer.errors)
    

class UserAuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permission(self):
        if self.action== 'logout_user':
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()
    
    def register_user(self,request,*args,**kwargs):

        serializer = UserSerializer(data=request.data)

        if request.user.is_authenticated:
            return Response("User already logged in.", status=403)
        
        # if User.objects.filter(username = serializer.username).exists():
        #         return Response("A user with that username already exists", status=403)
            
        # if User.objects.filter(email = user_instance.email).exists():
        #         return Response("A user with that email already exists", status=403)

        if serializer.is_valid():
            user_instance = serializer.save()
            token,created= Token.objects.get_or_create(user=user_instance)

            return Response({
                "user":{
                "id":user_instance.id,
                "username":user_instance.email,
                "email":user_instance.email,
                "full_name":user_instance.full_name
                },
                "token":token.key
            })
        
        else:
            return Response(serializer.errors, status=400)
        # user = User.objects.create(
        #     username = request.data.get("email"),
        #     email = request.data.get("email"),
        #     full_name = request.data.get("full_name")
        # )

        def create(self, request, *args, **kwargs):
            super().create(request, *args, **kwargs)
            return Response(self.response_data)
        

    # def logout_user(self,request,*args, **kwargs):
    #     # token = Token.objects.get(user=request.user)
    #     token = request.user.auth_token.delete()
    #     # token.delete()


    #     return Response("Logout successful")


    

    def login_user(self, request, *args,**kwargs):

        if request.user.is_authenticated:
            return Response("User already logged in.", status=403)
        username = request.data.get('email')
        password = request.data.get('password')

        #authenticate the user

        user = authenticate(username=username,password=password)

        if not user :
            # raise AuthenticationFailed("Invalid username or password")
            return Response("Username/password are required",status=401)
        

        #generate or retrieve token

        token,created= Token.objects.get_or_create(user=user)

        return Response({"user":{
            "id":user.id,
            "email":user.email,
        },"token":token.key})
    


class UserList(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self,request):
        user = request.user
        if user.is_staff or user.is_superuser:
            returnedUser = self.queryset
        else:
            returnedUser= self.queryset.filter(id=user.id)
        serializer = self.serializer_class(returnedUser, many = True)
        return Response(serializer.data)
    

# class UserList(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]
#     query_set = User.objects.all()

#     serializer_class = UserSerializer

#     def list(self,request):
#         query_set = self.query_set
#         serializer = self.serializer_class(query_set,many=True)
#         return Response(serializer.data)


class UserProfile(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def retrieve_user_profile(self,request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)




class VisitingData(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    query_set = visitingData.objects.all()
    serializer_class = visitingDataSerializer

    def create(self,request,*args, **kwargs):
        serializer = visitingDataSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

