# Generated by Django 2.2.1 on 2019-05-23 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("menu", "0013_auto_20190507_0309")]

    operations = [
        migrations.AlterField(
            model_name="menuitem",
            name="sort_order",
            field=models.PositiveIntegerField(db_index=True, editable=False, null=True),
        )
    ]
