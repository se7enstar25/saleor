# Generated by Django 2.1.2 on 2018-10-23 08:19

from django.db import migrations
from saleor.order import OrderEvents

def change_released_to_voided_in_order_events(apps, schema):
    PAYMENT_RELEASED = 'released'
    OrderEvent = apps.get_model('order', 'OrderEvent')
    OrderEvent.objects.filter(
        type=PAYMENT_RELEASED).update(type=OrderEvents.PAYMENT_VOIDED.value)


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0066_auto_20181023_0317'),
    ]

    operations = [
        migrations.RunPython(
            change_released_to_voided_in_order_events,
            migrations.RunPython.noop),
    ]
