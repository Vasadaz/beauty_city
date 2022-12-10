from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from beauty_shop.views import index, service, manager, notes

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('service/', service, name='service'),
    # path('api/consultation/', consultation, name='consultation'),
    path('manager/', manager, name='manager'),
    path('notes/', notes, name='notes'),

    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]


