from datetime import date
from django.shortcuts import render
from django.conf import settings
from .models import Salon, Category, Service, Master, Client, Feedback, Note
import requests
from textwrap import dedent


def service(request):
    salons = Salon.objects.all()
    categories = Category.objects.prefetch_related('services')
    masters = Master.objects.all()
    data = {
        'salons': salons,
        'categories': categories,
        'masters': masters
    }
    return render(request, 'service.html', context=data)


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


def service_finally(request, pk):
    note = Note.objects.get(id=pk)
    data = {'note': note}
    return render(request, 'serviceFinally.html', context=data)


# def get_master_slots(request, pk):
#     category_services = Master.objects.filter(id=pk).first()
#     print(category_services)
#     date1 = date.today()
#     print(category_services.notes.filter(date_time_start__day=date1.day))
#     return render(request, 'service.html', context={'category_services': category_services})


def manager(request):
    pass


def notes(request):
    pass
