from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from beauty_shop.views import index, service, manager, notes, service_finally

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('service/', service, name='service'),
    path('service/<pk>', service_finally, name='service_finally'),
    path('manager/', manager, name='manager'),
    path('notes/', notes, name='notes'),

    path('service_finally', service_finally, name='service_finally'),

    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
