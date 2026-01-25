from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from rest_framework.response import Response


class UserCart(viewsets.ViewSet):
     serializer_class = CartSerializer
     permission_classes = [permissions.IsAuthenticated]
     def get(self,request):
         
         user_obj,_ = Cart.objects.get_or_create(user = request.user)
         print(user_obj)
         serializer = self.serializer_class(user_obj)

         return Response(serializer.data)
     
     

class TourCartItemViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = TourCartItem.objects.all()
    serializer_class = TourCartItemSerializer

    def list(self,request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many = True)
        return Response(serializer.data)
    
    def addtocart(self, request,*args, **kwargs):
        
        spot_id = request.data.get('touristSpot')
        print(f"user : {request.user}")

        if not spot_id :
            return Response("Spot ID required", status=400)
        
        try:
            self.permission_classes = [permissions.IsAuthenticated]
            spot = addAttractions.objects.get(my_id = spot_id)
            cart,_ = Cart.objects.get_or_create(user = request.user)
            
            serializer = self.serializer_class(data=request.data)
            # print(serializer)
            if serializer.is_valid():
                
                serializer.save(cart=cart, touristSpot=spot)
                return Response(serializer.data, status=201)
            
            return Response("Invalid Data", serializer.errors)
        
        except addAttractions.DoesNotExist:
            return Response("Attractions not found",status=400)
        
        except Exception as e:
            return Response({
                "message": "An error occured when added item to cart",
                "error": str(e)
                }, status=500)
        
    def updatecart_item(self,request, pk=None):
        cartitem = TourCartItem.objects.get(cart__user = request.user.id, pk = pk)
        print(f"update cartitem:{cartitem}")
        serializer = CartSerializer( cartitem, data = request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

    def remove_item(self,request,pk=None):
        try:
            cartitem = TourCartItem.objects.get(cart__user = request.user,pk=pk)
            cartitem.delete()
            return Response("Item removed from cart",status=204)
        except cartitem.DoesNotExist:
            return Response("Item not found in your cart",status=404)
        except Exception as e:
            return Response({
                "message": "An error occured when added item to cart",
                "error": str(e)
                }, status=500)



    def clear_cart(self,request):
        try:
            cart = Cart.objects.get(user = request.user)
            TourCartItem.objects.filter(cart = cart).delete()
            return Response("Cart cleared successfully", status=204)
        except Cart.DoesNotExist:
            return Response("Cart not found", status = 404)
        
        except Exception as e:
            return Response({
                "message": "An error occured when clearing cart",
                "error": str(e)
                }, status=500)




# Error when hitting logout
# Forbidden (403)
# CSRF verification failed. Request aborted.

# Help
# Reason given for failure:

#     CSRF token from POST incorrect.
    
# In general, this can occur when there is a genuine Cross Site Request Forgery, or when Django’s CSRF mechanism has not been used correctly. For POST forms, you need to ensure:

# Your browser is accepting cookies.
# The view function passes a request to the template’s render method.
# In the template, there is a {% csrf_token %} template tag inside each POST form that targets an internal URL.
# If you are not using CsrfViewMiddleware, then you must use csrf_protect on any views that use the csrf_token template tag, as well as those that accept the POST data.
# The form has a valid CSRF token. After logging in in another browser tab or hitting the back button after a login, you may need to reload the page with the form, because the token is rotated after a login.
# You’re seeing the help section of this page because you have DEBUG = True in your Django settings file. Change that to False, and only the initial error message will be displayed.

# You can customize this page using the CSRF_FAILURE_VIEW setting.

