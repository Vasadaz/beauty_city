from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from beauty_shop.views import index, service, consultation

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('service/', service, name='service'),
    path('consultation/', consultation, name='consultation'),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]


