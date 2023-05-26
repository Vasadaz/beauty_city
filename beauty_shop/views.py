import requests

from django.conf import settings
from django.shortcuts import render
from textwrap import dedent
from datetime import datetime  
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
    all_note = Note.objects.all()
    current_month_visits = all_note.filter(
            date_time_start__month = datetime.today().month,
            ) 
    visits_per_year = all_note.filter(
            date_time_start__year = datetime.today().year,
            payment = True,
            ).count()
    monthly_total = sum(
            [
                visit.service.price for visit in current_month_visits.filter(
                    payment = True
                    )
                ]
            )
    paid_visits = current_month_visits.filter(payment = True).count()
    all_entries_month = all_note.count()
    visits_percentage = paid_visits * 100 / all_entries_month
    data = {
            'current_month_visits': paid_visits,
            'monthly_total': monthly_total,
            'visits_per_year': visits_per_year,
            'all_entries_month':all_entries_month,
            'visits_percentage': visits_percentage,
            }
    return render(request, 'manager.html', context=data)


def notes(request):
    return render(request, 'notes.html')


def popup(request):
    return render(request, 'popup.html')


def service(request):
    salons = Salon.objects.all()
    categories = Category.objects.prefetch_related('services')
    masters = Master.objects.all()
    data = {
        'salons': salons,
        'categories': categories,
    }
    if request.method == "POST":
        data['form'] = 'Получен POST'
        print('>' * 20, request.POST)

    return render(request, 'service.html', context=data)


def service_finally(request, pk):
    note = Note.objects.get(id=pk)
    data = {'note': note}
    if request.method == 'POST':
        fname = request.POST.get('fname', '')
        tel = request.POST.get('tel')

        if request.user:
            contactsTextarea = request.POST.get('contactsTextarea', '')
        else:
            client, created = Client.objects.get_or_create(
                name=fname,
                phonenumber=tel
            )
        note.message = contactsTextarea
        note.save()
    return render(request, 'service_finally.html', context=data)

