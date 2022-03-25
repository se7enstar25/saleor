# Generated by Django 3.2.12 on 2022-03-07 08:32

from django.db import migrations

BATCH_SIZE = 10000


def set_order_values(apps, _schema_editor):
    GiftCardEvent = apps.get_model("giftcard", "GiftCardEvent")
    Order = apps.get_model("order", "Order")

    queryset = GiftCardEvent.objects.filter(
        type__in=["used_in_order", "bought"]
    ).order_by("pk")
    for batch_pks in queryset_in_batches(queryset):
        gift_card_events = GiftCardEvent.objects.filter(pk__in=batch_pks)
        order_ids = gift_card_events.values_list("parameters__order_id", flat=True)
        orders_in_bulk = Order.objects.in_bulk(order_ids, field_name="number")
        for event in gift_card_events:
            order_id = event.parameters.pop("order_id", None)
            event.order = orders_in_bulk.get(order_id)

        GiftCardEvent.objects.bulk_update(gift_card_events, ["order", "parameters"])


def queryset_in_batches(queryset):
    """Slice a queryset into batches.

    Input queryset should be sorted be pk.
    """
    start_pk = 0

    while True:
        qs = queryset.filter(pk__gt=start_pk)[:BATCH_SIZE]
        pks = list(qs.values_list("pk", flat=True))

        if not pks:
            break

        yield pks

        start_pk = pks[-1]


class Migration(migrations.Migration):

    dependencies = [
        ("giftcard", "0013_giftcardevent_order"),
    ]

    operations = [
        migrations.RunPython(
            set_order_values,
            migrations.RunPython.noop,
        ),
    ]
