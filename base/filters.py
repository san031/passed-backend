import django_filters
from base.models import addAttractions

class SpotFilter(django_filters.FilterSet):
    class Meta:
        model = addAttractions
        fields = {'title': ['icontains'],
                  'location':['icontains'],
                  'category':['exact'],'price':['lt','gt'],'opening_time':['exact'],'closing_time':['exact']}