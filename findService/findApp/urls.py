from django.urls import path
from findApp import views

urlpatterns = [

    path('', views.home, name='home'),

]