# Generated by Django 4.1.3 on 2023-05-30 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beauty_shop', '0006_remove_client_surname_remove_note_payment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='payment_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на оплату'),
        ),
    ]
