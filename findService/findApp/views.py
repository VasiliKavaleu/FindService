from django.shortcuts import render
from .parsing import *
from .models import *

def home(request):
    autos = av()
    city = City.objects.get(name='Минск')
    carModel = CarModel.objects.get(name='Seat')
    a = Auto.objects.filter(city=city.id, carModel=carModel.id).values('url')
    url_list = [i['url'] for i in a]
    for newauto in autos:
        if newauto['href'] not in url_list:
            auto = Auto(city=city, carModel=carModel,
                        url=newauto['href'], title=newauto['name'],
                        description=newauto['desc'], price=newauto['price'])
            auto.save()
    return render(request, 'base.html', {"autos":autos})
