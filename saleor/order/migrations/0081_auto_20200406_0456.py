# Generated by Django 3.0.4 on 2020-04-06 09:56

from django.db import migrations


def match_orders_with_users(apps, *_args, **_kwargs):
    Order = apps.get_model("order", "Order")
    User = apps.get_model("account", "User")

    orders_with_no_user = Order.objects.filter(user_email__isnull=False, user=None)

    for order in orders_with_no_user:
        try:
            new_user = User.objects.get(email=order.user_email)
        except User.DoesNotExist:
            continue
        order.user = new_user
        order.save(update_fields=["user"])


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0080_invoice"),
    ]

    operations = [
        migrations.RunPython(match_orders_with_users),
    ]
