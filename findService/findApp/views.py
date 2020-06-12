from django.shortcuts import render
from django.http import Http404
from .parsing import *
from .models import *
from django.db import IntegrityError
import datetime
from findApp.forms import FindAutoForm
from findApp import helpers

def index(request):
    form = FindAutoForm
    return render(request, 'index1.html', {'form' : form})

def list_auto(request):
    today = datetime.date.today()
    form = FindAutoForm
    if request.GET:
        try:
            city_id = int(request.GET.get('city'))
            carModel_id = int(request.GET.get('carModel'))
        except ValueError:
            raise Http404('Страница не найдена')
        qs = Auto.objects.filter(city=city_id, carModel=carModel_id) #timestamp=today
        context = helpers.pg_records(request, qs, 5)
        context['form'] = form
        return render(request, 'findApp/list1.html', context)
    return render(request, 'findApp/list1.html', {'form':form})







def list_auto_today(request):
    today = datetime.date.today()
    city = City.objects.get(name='Минск')
    carModel = CarModel.objects.get(name='Seat')
    qs = Auto.objects.filter(city=city.id, carModel=carModel.id, timestamp=today)
    if qs:
        return render(request, 'findApp/list.html', {"autos": qs})
    return render(request, 'findApp/list.html')

def home(request):
    city = City.objects.get(name='Минск')
    carModel = CarModel.objects.get(name='Seat')
    site = Site.objects.all()
    url_qs = Url.objects.filter(city=city, carModel=carModel)
    url_av = url_qs.get(site=site.get(name='av.by'))
    autos = av(url_av.url_adress)
    for newauto in autos:
        auto = Auto(city=city, carModel=carModel,
                    url=newauto['href'], title=newauto['name'],
                    description=newauto['desc'], price=newauto['price'])
        try:
            auto.save()
        except IntegrityError:
            pass
    return render(request, 'findApp/list.html', {"autos":autos})
