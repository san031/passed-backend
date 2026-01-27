from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from cart import views

urlpatterns = [
    path('tourcartitem/', views.TourCartItemViewSet.as_view({'get': 'list'})),
    path('addtocart/',views.TourCartItemViewSet.as_view({'post':'addtocart'})),
    path('UserCart/', views.UserCart.as_view({'get':'get'})),
    path('updatecart/<int:pk>/', views.TourCartItemViewSet.as_view({'patch':'updatecart_item'})),
    path('removecartitem/<int:pk>/', views.TourCartItemViewSet.as_view({'delete':'remove_item'})),
    path('clear/',views.TourCartItemViewSet.as_view({'delete':'clear_cart'}))
]
