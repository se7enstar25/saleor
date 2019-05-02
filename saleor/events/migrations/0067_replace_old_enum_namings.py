# Generated by Django 2.2 on 2019-05-02 14:10

from enum import Enum

from django.db import migrations


class OldOrderEvents(Enum):
    PLACED = 'placed'
    PLACED_FROM_DRAFT = 'draft_placed'
    OVERSOLD_ITEMS = 'oversold_items'
    ORDER_MARKED_AS_PAID = 'marked_as_paid'
    CANCELED = 'canceled'
    ORDER_FULLY_PAID = 'order_paid'
    UPDATED = 'updated'

    EMAIL_SENT = 'email_sent'

    PAYMENT_CAPTURED = 'captured'
    PAYMENT_REFUNDED = 'refunded'
    PAYMENT_VOIDED = 'voided'

    FULFILLMENT_CANCELED = 'fulfillment_canceled'
    FULFILLMENT_RESTOCKED_ITEMS = 'restocked_items'
    FULFILLMENT_FULFILLED_ITEMS = 'fulfilled_items'
    TRACKING_UPDATED = 'tracking_updated'
    NOTE_ADDED = 'note_added'

    OTHER = 'other'


def _replace_old_namings(apps, *_args, **_kwargs):
    cls = apps.get_model('events', 'OrderEvent')

    for event_type in OldOrderEvents:
        for event in cls.objects.filter(type=event_type.value).all():
            event.type = event_type.name.lower()
            event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0066_auto_20190502_0910'),
    ]

    operations = [
        migrations.RunPython(_replace_old_namings)
    ]
