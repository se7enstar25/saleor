# Generated by Django 3.2.14 on 2022-07-15 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0015_app_manifest_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appextension",
            name="mount",
            field=models.CharField(
                choices=[
                    ("customer_overview_create", "customer_overview_create"),
                    (
                        "customer_overview_more_actions",
                        "customer_overview_more_actions",
                    ),
                    ("customer_details_more_actions", "customer_details_more_actions"),
                    ("product_overview_create", "product_overview_create"),
                    ("product_overview_more_actions", "product_overview_more_actions"),
                    ("product_details_more_actions", "product_details_more_actions"),
                    ("navigation_catalog", "navigation_catalog"),
                    ("navigation_orders", "navigation_orders"),
                    ("navigation_customers", "navigation_customers"),
                    ("navigation_discounts", "navigation_discounts"),
                    ("navigation_translations", "navigation_translations"),
                    ("navigation_pages", "navigation_pages"),
                    ("order_details_more_actions", "order_details_more_actions"),
                    ("order_overview_create", "order_overview_create"),
                    ("order_overview_more_actions", "order_overview_more_actions"),
                ],
                max_length=256,
            ),
        ),
    ]
