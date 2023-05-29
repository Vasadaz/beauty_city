import locale
from datetime import datetime, timedelta
from textwrap import dedent

import requests

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from .models import (
    Salon,
    Category,
    Service,
    Master,
    Client,
    Feedback,
    Note,
)

locale.setlocale(
    category=locale.LC_ALL,
    locale='',
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
        url = f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendmessage'
        params = {'chat_id': settings.TELEGRAM_CHAT_ID, 'text': dedent(msg)}
        response = requests.get(url, params=params)
        response.raise_for_status()
    return render(request, 'index.html', context=data)


def manager(request):
    if not request.user.is_superuser:
        return redirect('http://127.0.0.1:8000/admin/login/?next=/manager/')
    all_note = Note.objects.all()
    current_month_visits = all_note.filter(
        date_time_start__month=datetime.today().month,
    )
    visits_per_year = all_note.filter(
        date_time_start__year=datetime.today().year,
        payment=True,
    ).count()
    monthly_total = sum(
        [
            visit.service.price for visit in current_month_visits.filter(
            payment=True
        )
        ]
    )
    paid_visits = current_month_visits.filter(payment=True).count()
    all_entries_month = all_note.count()
    visits_percentage = paid_visits * 100 // all_entries_month
    data = {
        'current_month_visits': paid_visits,
        'monthly_total': monthly_total,
        'visits_per_year': visits_per_year,
        'all_entries_month': all_entries_month,
        'visits_percentage': visits_percentage,
    }
    return render(request, 'manager.html', context=data)


def notes(request):
    if request.method == 'POST':
        salon = Salon.objects.get(id=request.POST.get('salon'))
        service = Service.objects.get(id=request.POST.get('service'))
        master = Master.objects.get(id=request.POST.get('master'))

        client_name = request.POST.get('client_name')
        client_tel = request.POST.get('client_tel')
        client_comment = request.POST.get('client_comment', '')

        date_time_start = datetime.strptime(request.POST.get('datetime'), '%d %B %Y (%A) %H:%M')
        print(date_time_start)

        client_obj, created_as = Client.objects.get_or_create(
            phonenumber=client_tel,
            name=client_name,
        )

        if created_as:
            client_obj.name = client_name
            client_obj.surname = ''
            client_obj.save()


        note_obj = Note(
            client=client_obj,
            master=master,
            service=service,
            salon=salon,
            comment=client_comment,
            date_time_start=date_time_start,
            date_time_end=date_time_start,
            payment=True,
        )
        note_obj.save()


    return JsonResponse(request.POST)
    #return render(request, 'notes.html')


def popup(request):

    return render(request, 'popup.html')


def service(request):
    salons = Salon.objects.all()
    categories = Category.objects.prefetch_related('services')
    masters = Master.objects.all()
    master_time_slots = {}

    for master in masters:
        time_slots = {}

        for slot in master.time_slots.all():
            date_at = slot.time_slot_at.strftime('%d %B %Y (%A)')
            time_at = slot.time_slot_at.strftime('%H:%M')

            if not time_slots.get(date_at):
                time_slots[date_at] = []

            time_slots[date_at].append(time_at)

        master_time_slots[master.id] = time_slots

    data = {
        'salons': salons,
        'categories': categories,
        'masters': masters,
        'master_time_slots': master_time_slots
    }

    return render(request, 'service.html', context=data)


def service_finally(request):
    if request.method == 'POST':
        salon = Salon.objects.get(id=request.POST.get('salon'))
        service = Service.objects.get(id=request.POST.get('service'))
        master = Master.objects.get(id=request.POST.get('master'))
        date = request.POST.get('date')
        time = request.POST.get('time')

        data = {
            'salon': salon,
            'service': service,
            'master': master,
            'date': date,
            'time': time,
        }


    return render(request, 'service_finally.html', context=data)



"""
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
"""
