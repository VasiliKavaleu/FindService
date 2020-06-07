from django.shortcuts import render
from findApp.forms import FindAutoForm

def index(request):
    form = FindAutoForm
    return render(request, 'findApp/list.html', {'form' : form})
    # return render(request, 'base.html')