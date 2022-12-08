from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from .models import Category, Client, Feedback, Master, Note, Salon, Service


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )
    list_per_page = 15


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'address',
    )
    list_per_page = 15


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'category',
        'duration',
        'price',
        'image',
        'image_preview',
    ]
    list_display = (
        'title',
        'duration',
        'price',
        'image_preview',
    )
    list_filter = ('category',)
    list_per_page = 15
    # raw_id_fields = ('category',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        output = format_html('<img src="{0}" style="height: {1}px"/>', obj.image.url, 100)
        return mark_safe(output)

    image_preview.short_desciption = 'Предосмотр картинки'


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'surname',
        'salon',
    )
    list_per_page = 15


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'surname',
        'phonenumber',
    )
    list_per_page = 15


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'client',
        'master',
        'assessment',
    )
    list_filter = (
        'client',
        'master',
        'assessment',
    )
    list_per_page = 15


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        'client',
        'master',
        'service',
        'date_time_start',
    )
    list_filter = (
        'client',
        'master',
        'service',
        'salon',
    )
    list_per_page = 15
