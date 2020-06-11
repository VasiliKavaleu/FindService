from django.shortcuts import render
from django.http import Http404
from .parsing import *
from .models import *
from django.db import IntegrityError
import datetime
from findApp.forms import FindAutoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    form = FindAutoForm

    return render(request, 'index1.html', {'form' : form})
    # return render(request, 'index.html', {'form' : form})

def list_auto(request):
    today = datetime.date.today()
    form = FindAutoForm
    if request.GET:
        try:
            city_id = int(request.GET.get('city'))
            carModel_id = int(request.GET.get('carModel'))
        except ValueError:
            raise Http404('Страница не найдена')
        context = {}
        context['form'] = form
        qs = Auto.objects.filter(city=city_id, carModel=carModel_id) #timestamp=today
        paginator = Paginator(qs, 5)
        page = request.GET.get('page')
        try:
            qs_paginator = paginator.page(page)
        except PageNotAnInteger:
            qs_paginator = paginator.page(1)
        except EmptyPage:
            qs_paginator = paginator.page(paginator.num_pages)

        print(paginator.page_range)

        is_qs_paginated = qs_paginator.has_other_pages()

        if qs_paginator.has_previous():
            prev_page = f"&page={qs_paginator.previous_page_number()}"
        else:
            prev_page = ""
        if qs_paginator.has_next():
            next_page = f"&page={qs_paginator.next_page_number()}"
        else:
            next_page = ""
        # if qs_paginator:
        #     context = {
        #         'is_qs_paginated' : is_qs_paginated,
        #         'next_page' : next_page,
        #         'prev_page' : prev_page,
        #         'autos' : qs_paginator,
        #         'city' : qs_paginator[0].city,
        #         'carModel' : qs_paginator[0].carModel
        #     }
        if qs:
            # context['paginator'] = paginator
            context['is_qs_paginated'] = is_qs_paginated
            context['prev_page'] = prev_page
            context['next_page'] = next_page
            context['autos'] = qs_paginator
            context['city'] = qs_paginator[0].city
            context['carModel'] = qs_paginator[0].carModel


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
    return render(request, 'findApp/list.html', {"autos":autos})
