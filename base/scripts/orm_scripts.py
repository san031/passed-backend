from base.models import addAttractions,visitingData,User,buyPass
from django.db import connection
from pprint import pprint
def run():
    # print(addAttractions.objects.filter(title__startswith = 'Taj'))
    # print(addAttractions.objects.all())

    # print(visitingData.objects.values('members','start_date'))
    # print(visitingData.objects.select_related('visitingSpot').all())
    # print(User.objects.values('email'))
    # print(buyPass.objects.select_related('user').all())
    # print(addAttractions.objects.filter(category = 'LIBRARY',title__startswith = 'T'))
    # print(addAttractions.objects.filter(category = addAttractions.chooseCategory.library))

    # check_category = ['park','temple','meuseum','historic_monument','library']
    # print(addAttractions.objects.filter(category__in = check_category))

    # print(addAttractions.objects.filter(is_featured = True))
    pprint(connection.queries)


    