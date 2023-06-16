from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from beauty_shop.views import (
    index,
    manager,
    note,
    notes,
    check_payment,
    service,
    service_finally,
)
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('manager/', manager, name='manager'),
    path('note/', note, name='note'),
    path('notes/<pk>/', notes, name='notes'),
    path('service/', service, name='service'),
    path('service_finally/', service_finally, name='service_finally'),
    path('check_payment/<pk>/', check_payment, name='check_payment'),

    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
