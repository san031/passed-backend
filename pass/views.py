from rest_framework import viewsets,permissions
from .serializers import *
from .models import *
from rest_framework.response import Response
from cart.models import Cart,TourCartItem



class passedViewset(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = passedSerializer
    queryset = passed.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        return queryset.filter(user = user)
    
    def list(self,request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many= True)
        return Response(serializer.data)
    
    def generatepasscode(self,request,*args,**kwargs):

        user = request.user
        cart_id = self.kwargs.get('id')

        
        userPass = passed.objects.create(user = user)
        cart_items = TourCartItem.objects.filter(cart__user = user)
        # members = TourCartItem.objects.filter(cart__user = user, )
        print(f"userPass : {userPass}")
        print(f"cart_items:{cart_items}")
        for item in cart_items:
            print(item.touristSpot, item.members, item.start_date, item.end_date)
            # temp,_ = cartedSpots.objects.get_or_create(tourist_spots = item.touristSpot )
            cartedSpots.objects.create(
                userPass = userPass,
                tourist_spots = item.touristSpot,
                members = item.members,
                start_date = item.start_date,
                end_date = item.end_date
            )
            # spots_cart.append(temp)
        # userPass = request.data.get('cart.user')
        # print(f"spots_cart is me : {spots_cart}")
        print(f"requested user : {request.user}")
        print(f"cart_items : {cart_items}")

        
        try:
            
            # qs,_ = passed.objects.get_or_create(user = request.user)
            print(request.data)
            cart_items.delete()
            serializer = self.serializer_class(userPass, many=True)
            # print(serializer)
                # print(serializer.data)
            return Response(serializer.data, status=201)
            
            
        except Exception as e:
            return Response({
                "message": "An error occured while generating pass",
                "error": str(e)
                }, status=500)
            
        
        

# this is json data {

    # "id": 8,

    # "user": 4,

    # "pass_code": "FA751396",

    # "cart_spots": null,

    # "spots_cart": null}



# cart_spots is declared as foreign key to CartedSpots and then it is further related as OnetoOne field to addAttractions, what id should be passed to cart_spots field