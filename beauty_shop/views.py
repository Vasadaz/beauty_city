from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


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

