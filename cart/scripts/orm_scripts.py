from cart.models import TourCartItem,Cart
from pprint import pprint
from django.db import connection

def run():
    # print(TourCartItem.objects.values('start_date'))
    # print(Cart.objects.values('user_id'))
    # print(Cart.objects.create(user  = 'testvite@gmail.com'))
    # print(Cart.objects.select_related('user').all())
    # print(TourCartItem.objects.select_related('touristSpot').all())
    # print(TourCartItem.objects.values('touristSpot'))
    # print(TourCartItem.objects.values_list('touristSpot',flat=True))
    # print(TourCartItem.objects.get('touristSpot'))
    pprint(connection.queries)
