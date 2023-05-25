from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from beauty_shop.views import (
    index,
    manager,
    notes,
    popup,
    service,
    service_finally,
)
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('manager/', manager, name='manager'),
    path('notes/', notes, name='notes'),
    path('popup/', popup, name='popup'),
    path('service/', service, name='service'),
    path('service/<pk>', service_finally, name='service_finally'),
    path('service_finally', service_finally, name='service_finally'),

    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
