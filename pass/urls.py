from django.urls import path
from .views import *

urlpatterns = [
    path('viewpass/', passedViewset.as_view({'get': 'list'})),
    path('passed/',passedViewset.as_view({'post':'generatepasscode'})),
]