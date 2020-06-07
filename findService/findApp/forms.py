from django import forms
from findApp.models import CarModel, City

class FindAutoForm(forms.Form):
    city = forms.ModelChoiceField(label='Город', queryset=City.objects.all(),
                                  widget=forms.Select(attrs={'class':'form-control addedstyle', 'name':'city'}))
    carModel = forms.ModelChoiceField(label='Марка авто', queryset=CarModel.objects.all(),
                                  widget=forms.Select(attrs={'class':'form-control', 'name':'model'}))