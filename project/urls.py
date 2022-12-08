from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from beauty_shop.views import get_salons, get_salon, get_categories, get_category, get_services, get_service, get_masters, get_master,\
    get_clients, get_client, get_feedbacks, get_feedback, get_notes, get_note, get_category_services, get_master_slots, get_salon_masters

urlpatterns = [
    path('admin/', admin.site.urls),

    path('salons/', get_salons, name='salons_list'),
    path('salons/<pk>', get_salon, name='salon_detail_info'),
    path('salons/<pk>/masters', get_salon_masters, name='salon_masters_list'),

    path('categories/', get_categories, name='categories_list'),
    path('categories/<pk>', get_category, name='category_detail_info'),
    path('categories/<pk>/services', get_category_services, name='category_services_list'),

    path('services/', get_services, name='services_list'),
    path('services/<pk>', get_service, name='service_detail_info'),

    path('masters/', get_masters, name='masters_list'),
    path('masters/<pk>', get_master, name='master_detail_info'),
    path('masters/<pk>/slots', get_master_slots, name='master_slots_info'),

    path('clients/', get_clients, name='clients_list'),
    path('clients/<pk>', get_client, name='client_detail_info'),

    path('feedbacks/', get_feedbacks, name='feedbacks_list'),
    path('feedbacks/<pk>', get_feedback, name='feedback_detail_info'),

    path('notes/', get_notes, name='notes_list'),
    path('notes/<pk>', get_note, name='note_detail_info'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
