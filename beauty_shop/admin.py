from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from .models import Category, Client, Feedback, Master, Note, Salon, Service


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )
    list_per_page = 20


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'address',
        'preview',
    )
    list_per_page = 20
    readonly_fields = ('preview',)

    @admin.display(description='Превью изображения')
    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;">')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'category',
        'duration',
        'price',
        'image',
        'preview',
    ]
    list_display = (
        'title',
        'duration',
        'price',
        'preview',
    )
    list_filter = ('category',)
    list_per_page = 20
    # raw_id_fields = ('category',)
    readonly_fields = ('preview',)

    @admin.display(description='Превью изображения')
    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;">')


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'surname',
        'salon',
        'profession',
        'preview',
    )
    list_per_page = 20
    readonly_fields = ('preview',)

    @admin.display(description='Превью изображения')
    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;">')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'surname',
        'phonenumber',
    )
    list_per_page = 20


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'client',
        'master',
        'rating',
    )
    list_filter = (
        'client',
        'master',
        'rating',
    )
    list_per_page = 20


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
    list_per_page = 20
