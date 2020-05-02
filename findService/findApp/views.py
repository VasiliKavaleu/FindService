from django.shortcuts import render
from .parsing import *
from .models import *
from django.db import IntegrityError

def home(request):
    city = City.objects.get(name='Минск')
    carModel = CarModel.objects.get(name='Seat')
    site = Site.objects.all()

    url_qs = Url.objects.filter(city=city, carModel=carModel)
    url_av = url_qs.get(site=site.get(name='av.by'))


    autos = av(url_av.url_adress)

    # a = Auto.objects.filter(city=city.id, carModel=carModel.id).values('url')
    # url_list = [i['url'] for i in a]
    for newauto in autos:
        # if newauto['href'] not in url_list:
        auto = Auto(city=city, carModel=carModel,
                    url=newauto['href'], title=newauto['name'],
                    description=newauto['desc'], price=newauto['price'])
        try:
            auto.save()
        except IntegrityError:
            pass
    return render(request, 'base.html', {"autos":autos})
