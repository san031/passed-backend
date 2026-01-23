from django.urls import path,include
from .views import *
from base import views
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt import TokenRefreshView


# router=DefaultRouter()
# router.register('buypass',BuyPassViewSet, basename='buypass')
# router.register('register',RegisterView, basename='register')
# router.register(r'addAttractions', AddAttractionsViewSet, basename='addAttractions')

# urlpatterns = router.urls
# urlpatterns = [
#     path('', include(router.urls)),]


urlpatterns = [
    path('buypass/', views.BuyPassViewSet.as_view({'get': 'list'},)  ),
    # path('createpass/', views.BuyPassViewSet.as_view({'post': 'post'},)  ),

    # path('register/',views.RegisterView.as_view()),
    path('register/',views.UserAuthViewSet.as_view({'post':'register_user'}), name='register'),
    path('login/',views.UserAuthViewSet.as_view({'post':'login_user'})),
    # path('logout/',views.UserAuthViewSet.as_view({'post':'logout_user'})),
    path('user/',UserList.as_view({'get':'list'})),
    path('addAttractions/',AddAttractionsViewSet.as_view({'get': 'list'})),
    path('profile/',views.UserProfile.as_view({'get':'retrieve_user_profile'})),
    path('addAttractions/<int:pk>/',AddAttractionsViewSet.as_view({'get':'retrieve_spot'})),
    path('addAttractions/<int:pk>/visitingData/', views.VisitingData.as_view({'post' : 'create'})),
    path('featuredSpots/', AddAttractionsViewSet.as_view({'get':'featuredSpots'}))
]