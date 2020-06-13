from django.shortcuts import render, redirect, get_object_or_404
from .forms import SubscriberModelForm, LogInForm, SubscriberHiddenEmailForm, ContactForm
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Subscriber
from findService.secret import ADMIN, MAILGUN_KEY, API, FROM_EMAIL
import requests

class SubscriberCreate(CreateView):
    model = Subscriber
    form_class = SubscriberModelForm
    template_name = 'subscribers/create1.html'
    success_url = reverse_lazy('create')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            messages.success(request, 'Data saved successfully!')
            return self.form_valid(form)
        else:
            messages.error(request, 'Check that the form is filled out correctly!')
            return self.form_invalid(form)

def create_user(request):
    if request.method == "GET":
        form = SubscriberModelForm
        return render(request, 'subscribers/create1.html', {'form':form} )
    elif request.method == "POST":
        form = SubscriberModelForm(request.POST or None)
        if form.is_valid():
            form.save()
            msg = 'Data saved successfully! You have subscribed to receive updates of new arrivals on choosen category.'
            messages.success(request, msg)
            return redirect('create')
        messages.error(request, 'Check that the form is filled out correctly! Perhaps, this email exists afore.')
        return render(request, 'subscribers/create1.html', {'form':form} )





def login_subscriber(request):
    if request.method == "GET":
        form = LogInForm
        return render(request, 'subscribers/login1.html', {'form':form} )
    elif request.method == "POST":
        form = LogInForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            request.session['email'] = data['email']
            return redirect('update')
        return render(request, 'subscribers/login1.html', {'form': form})


def update_subscriber(request):
    if request.method == 'GET' and request.session.get('email', False):
        email = request.session.get('email')
        print(email)
        qs = Subscriber.objects.filter(email=email).first()
        if not qs:
            return redirect('login') # TESTING

        form = SubscriberHiddenEmailForm(initial={'email':qs.email, 'city':qs.city,    #
                                                  'carModel':qs.carModel, 'password':qs.password,
                                                  'is_activ':qs.is_activ})
        return render(request, 'subscribers/update1.html', {'form': form})
    elif request.method == 'POST':
        email = request.session.get('email')
        user = get_object_or_404(Subscriber, email=email)
        form = SubscriberHiddenEmailForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data saved successfully!')
            del request.session['email']
            return redirect('index')
            #return redirect('login')
        messages.error(request, 'Check that the form is filled out correctly!')
        return render(request, 'subscribers/update1.html', {'form': form})
    else:
        return redirect('login')

def contact_admin(request):
    if request.method == 'POST':
        form = ContactForm(request.post or None)
        if form.is_valid():
            city = form.cleaned_data['city']
            carModel = form.cleaned_data['carModel']
            from_email = form.cleaned_data['email']
            content = f'Прошу добавиь в поиск, город {city}, авто {carModel}. Запрос от пользователя {email}'
            Subject = 'Запрос на добавление в БД'
            requests.post(API,
                          auth=("api", MAILGUN_KEY),
                          data={"from": from_email,
                                "to": ADMIN,
                                "subject": Subject,
                                "text": content})
            messages.error(request, 'Ваше письмо отправлено!')
            return redirect('index1')
        return render(request, 'subscribers/contact.html', {'form': form})
    else:
        form = ContactForm
    return render(request, 'subscribers/contact.html', {'form': form})