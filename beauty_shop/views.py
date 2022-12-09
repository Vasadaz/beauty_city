from datetime import date
from django.shortcuts import render

from .models import Salon, Category, Service, Master, Client, Feedback, Note


def service(request):
    salons = Salon.objects.all().values()
    categories = Category.objects.all().values()
    # category_services = Service.objects.filter(category=pk).values()
    services = Service.objects.all().values()
    # salon_masters = Master.objects.filter(salon=pk).values()
    data = {
        'salons': salons,
        'categories': categories,
        # 'category_services': category_services,
        'services': services,
    }
    return render(request, 'service.html', context={'data': data})


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
    return render(request, 'index.html', context=data)


# def get_master_slots(request, pk):
#     category_services = Master.objects.filter(id=pk).first()
#     print(category_services)
#     date1 = date.today()
#     print(category_services.notes.filter(date_time_start__day=date1.day))
#     return render(request, 'service.html', context={'category_services': category_services})

def consultation(request):
    pass


def manager(request):
    pass


def notes(request):
    pass
