import requests

from django.conf import settings
from django.shortcuts import render
from textwrap import dedent

from .models import (
    Salon,
    Category,
    Service,
    Master,
    Client,
    Feedback,
    Note,
)


def index(request):
    salons = Salon.objects.all()
    services = Service.objects.all()
    masters = Master.objects.all()
    feedbacks = Feedback.objects.all()
    data = {
        'salons': salons,
        'services': services,
        'masters': masters,
        'feedbacks': feedbacks,
    }
    if request.method == 'POST':
        user_name = request.POST.get('fname', '')
        user_tel = request.POST['tel']
        order_text = request.POST.get('contactsTextarea', '')
        msg = f'''
        Заявка на консультацию:
        Имя: {user_name}
        Телефон: {user_tel}
        Сообщение: {order_text}'''
        url = f"https://api.telegram.org/bot{settings.TOKEN_TG}/sendmessage"
        params = {'chat_id': settings.CHAT_ID, 'text': dedent(msg)}
        response = requests.get(url, params=params)
        response.raise_for_status()
    return render(request, 'index.html', context=data)


def manager(request):
    return render(request, 'manager.html')


def notes(request):
    return render(request, 'notes.html')


def popup(request):
    return render(request, 'popup.html')


def service(request):
    return render(request, 'service.html')


def service_finally(request):
    return render(request, 'service_finally.html')

