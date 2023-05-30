import locale
import uuid

from datetime import datetime, timedelta
from pathlib import Path
from textwrap import dedent
from urllib.parse import urlparse, urlencode
import requests

from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse
from yookassa import Configuration, Payment

from beauty_shop.models import (
    Salon,
    Category,
    Service,
    Master,
    Client,
    Feedback,
    Note,
)
from project.settings import YOOMANEY_API_KEY, YOOMANEY_SHOP_ID

locale.setlocale(
    category=locale.LC_ALL,
    locale='ru_RU.UTF-8',
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
        #previous_url = Path(request.META.get('HTTP_REFERER'))
        #new_url = previous_url.parent / 'admin' / 'login'
        new_url = Path('https://vasadaz.ru') / 'admin' / 'login'
        payload = {'next': '/manager/'}
        parsed = urlparse(new_url.as_posix())
        merged_params = urlencode(payload)
        parsed = parsed._replace(query=merged_params)
        return_url = parsed.geturl()
        return redirect(return_url)
    all_note = Note.objects.all()
    current_month_visits = all_note.filter(
        date_time_start__month=datetime.today().month,
    )
    visits_per_year = all_note.filter(
        date_time_start__year=datetime.today().year,
        payment_status=True,
    ).count()
    monthly_total = current_month_visits.filter(payment_status=True).aggregate(Sum('price'))

    paid_visits = current_month_visits.filter(payment_status=True).count()
    all_entries_month = all_note.count()
    visits_percentage = paid_visits * 100 // all_entries_month
    data = {
        'current_month_visits': paid_visits,
        'monthly_total': monthly_total['price__sum'],
        'visits_per_year': visits_per_year,
        'all_entries_month': all_entries_month,
        'visits_percentage': visits_percentage,
    }
    return render(request, 'manager.html', context=data)


def get_payment_url(previous_url: Path, client_id: int, price: str, note_id: int = None, note_ids: list = None) -> str:
    Configuration.account_id = YOOMANEY_SHOP_ID
    Configuration.secret_key = YOOMANEY_API_KEY

    if note_ids:
        description = 'Заказы ' + ''.join([f' №{id},' for id in note_ids])[:-1]
        note_id = 0
    else:
        description = f'Заказ №{note_id}'

    new_url = previous_url.parent / 'check_payment' / str(client_id)
    payload = {'note': note_id}
    parsed = urlparse(new_url.as_posix())
    merged_params = urlencode(payload)
    parsed = parsed._replace(query=merged_params)
    return_url = parsed.geturl()

    payment = Payment.create({
        'amount': {
            'value': price,
            'currency': 'RUB'
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': return_url,
        },
        'capture': True,
        'description': description,
        'test': True,
    }, uuid.uuid4())

    return payment.confirmation.confirmation_url


def note(request):
    if request.method == 'POST':
        salon = Salon.objects.get(id=request.POST.get('salon'))
        service = Service.objects.get(id=request.POST.get('service'))
        master = Master.objects.get(id=request.POST.get('master'))

        client_name = request.POST.get('client_name')
        client_tel = request.POST.get('client_tel')
        client_comment = request.POST.get('client_comment', '')
        previous_url = Path(request.META.get('HTTP_REFERER'))

        date_time_start = datetime.strptime(request.POST.get('datetime'), '%d %B %Y (%A) %H:%M')
        date_time_end = date_time_start + timedelta(hours=service.duration.hour, minutes=service.duration.minute)

        for slot in master.time_slots.all():
            if date_time_start - timedelta(hours=1, minutes=30) <= slot.time_slot_at <= date_time_end:
                slot.delete()

        client_obj, created_as = Client.objects.get_or_create(
            phonenumber=client_tel,
        )

        if created_as:
            client_obj.name = client_name
            client_obj.save()

        note_obj = Note(
            client=client_obj,
            master=master,
            service=service,
            price=service.price,
            salon=salon,
            comment=client_comment,
            date_time_start=date_time_start,
            date_time_end=date_time_end,
        )
        note_obj.save()

        note_obj.payment_url = get_payment_url(
            previous_url=previous_url,
            client_id=client_obj.id,
            price=note_obj.price,
            note_id=note_obj.id,
        )
        note_obj.save()

        return redirect(reverse('notes', args=[client_obj.id]))


def notes(request, pk):
    client_obj = Client.objects.get(id=pk)

    try:
        price_sum = client_obj.notes.filter(payment_status=False).aggregate(Sum('price'))
        price_sum = price_sum['price__sum']
        note_ids = client_obj.notes.filter(payment_status=False).values_list('id', flat=True)
        previous_url = Path(request.META.get('HTTP_REFERER'))
        price_sum_url = get_payment_url(
            previous_url=previous_url,
            client_id=client_obj.id,
            price=price_sum,
            note_ids=note_ids,
        )
    except TypeError:
        price_sum = 0
        price_sum_url = '#'

    data = {
        'client': client_obj,
        'price_sum': price_sum,
        'price_sum_url': price_sum_url,
    }

    return render(request, 'notes.html', context=data)


def check_payment(request, pk):
    client_obj = Client.objects.get(id=pk)
    note = request.GET.get('note')

    if note != '0':
        note_obj = Note.objects.get(id=note)
        note_obj.payment_url = None
        note_obj.payment_status = True
        note_obj.save()
    else:
        for note_obj in client_obj.notes.filter(payment_status=False):
            note_obj.payment_url = None
            note_obj.payment_status = True
            note_obj.save()

    return redirect(reverse('notes', args=[client_obj.id]))


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
