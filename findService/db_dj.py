import os, sys
project_dir = os.path.dirname(os.path.abspath('db_bj.py'))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'findService.settings'
import django
django.setup()

from findApp.parsing import *
from findApp.models import *
from django.db import IntegrityError
import datetime
from subscribers.models import *

def get_all_car_model():
    qs = Subscriber.objects.filter(is_activ=True)
    todo_list = { i.city:set() for i in qs}
    for i in qs:
        todo_list[i.city].add(i.carModel)
    return todo_list

def get_urls(todo_list):
    url_list = []
    for city in todo_list:
        for model in todo_list[city]:
            tmp = {}
            qs = Url.objects.filter(city=city, carModel=model)
            if qs:
                tmp['city'] = city
                tmp['carModel'] = model
                for item in qs:
                    tmp[item.site.name] = item.url_adress
                url_list.append(tmp)
    return url_list

def scraping_sites():
    todo_list = get_all_car_model()
    url_list = get_urls(todo_list)
    autos = []
    for url in url_list:
        tmp = {}
        tmp_content = []
        tmp_content.extend(av(url['av.by']))
        tmp['city'] = url['city']
        tmp['carModel'] = url['carModel']
        tmp['content'] = tmp_content
        autos.append(tmp)
    return autos

def save_to_db():
    all_data = scraping_sites()
    if all_data:
        for data in all_data:
            city = data['city']
            carModel = data['carModel']
            autos = data['content']
            for auto in autos:
                car = Auto(city=city, carModel=carModel,
                            url=auto['href'], title=auto['name'],
                            description=auto['desc'], price=auto['price'])
                try:
                    car.save()
                except IntegrityError:
                    pass
        return True

print(save_to_db())