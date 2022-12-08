from datetime import date
from django.shortcuts import render
# from django.http import JsonResponse

from .models import Salon, Category, Service, Master, Client, Feedback, Note


def get_salons(request):
    salons = Salon.objects.all().values()
    return render(request, 'index.html', context={'places': salons})


def get_salon(request, pk):
    salon = Salon.objects.filter(id=pk).values()
    return render(request, 'index.html', context={'salon': salon})


def get_categories(request):
    categories = Category.objects.all().values()
    return render(request, 'service.html', context={'categories': categories})


def get_category(request, pk):
    category = Category.objects.filter(id=pk).values()
    return render(request, 'service.html', context={'category': category})


def get_services(request):
    services = Service.objects.all().values()
    return render(request, 'index.html', context={'services': services})


def get_service(request, pk):
    service = Service.objects.filter(id=pk).values()
    return render(request, 'index.html', context={'service': service})


def get_masters(request):
    masters = Master.objects.all().values()
    return render(request, 'index.html', context={'masters': masters})


def get_master(request, pk):
    master = Master.objects.filter(id=pk).values()
    return render(request, 'index.html', context={'master': master})


def get_clients(request):
    clients = Client.objects.all().values()
    return render(request, 'service.html', context={'clients': clients})


def get_client(request, pk):
    client = Client.objects.filter(id=pk).values()
    return render(request, 'service.html', context={'client': client})


def get_feedbacks(request):
    feedbacks = Feedback.objects.all().values()
    return render(request, 'index.html', context={'feedbacks': feedbacks})


def get_feedback(request, pk):
    feedback = Feedback.objects.filter(id=pk).values()
    return render(request, 'index.html', context={'feedback': feedback})


def get_notes(request):
    notes = Note.objects.all().values()
    return render(request, 'service.html', context={'notes': notes})


def get_note(request, pk):
    note = Note.objects.filter(id=pk).values()
    # return JsonResponse({'note': list(note)}, json_dumps_params={'indent': 4, 'ensure_ascii': False})
    return render(request, 'service.html', context={'note': note})


def get_category_services(request, pk):
    category_services = Service.objects.filter(category=pk).values()
    return render(request, 'service.html', context={'category_services': category_services})


def get_salon_masters(request, pk):
    salon_masters = Master.objects.filter(salon=pk).values()
    return render(request, 'service.html', context={'salon_masters': salon_masters})


def get_master_slots(request, pk):
    category_services = Master.objects.filter(id=pk).first()
    print(category_services)
    date1 = date.today()
    print(category_services.notes.filter(date_time_start__day=date1.day))
    return render(request, 'service.html', context={'category_services': category_services})