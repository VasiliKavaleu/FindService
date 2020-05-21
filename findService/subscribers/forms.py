from django import forms
from subscribers.models import Subscriber
from findApp.models import CarModel, City

class SubscriberModelForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    city = forms.ModelChoiceField(label='Город', queryset=City.objects.all(),
                                  widget=forms.Select(attrs={'class':'form-control'}))
    carModel = forms.ModelChoiceField(label='Марка авто', queryset=CarModel.objects.all(),
                                  widget=forms.Select(attrs={'class':'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = Subscriber
        fields = ('email', 'city', 'carModel', 'password')
        exclude = ('is_activ',)

class LogInForm(forms.Form):
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password(self, *args, **kwargs): # выполняется метод при вызове is_valid, формат наименования clean_ + переменная password
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            qs = Subscriber.objects.filter(email=email).first()
            if qs == None:
                raise forms.ValidationError('''Пользователь с таким e-mail не существует''')
            elif password != qs.password:
                raise forms.ValidationError('''Не верный пароль!''')

        return email

class SubscriberHiddenEmailForm(forms.ModelForm):
    city = forms.ModelChoiceField(label='Город', queryset=City.objects.all(),
                                  widget=forms.Select(attrs={'class':'form-control'}))
    carModel = forms.ModelChoiceField(label='Марка авто', queryset=CarModel.objects.all(),
                                  widget=forms.Select(attrs={'class':'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.HiddenInput())
    is_activ = forms.BooleanField(label='Получать рассылку?', required=False, widget=forms.CheckboxInput())

    class Meta:
        model = Subscriber
        fields = ('email', 'city', 'carModel', 'password', 'is_activ')