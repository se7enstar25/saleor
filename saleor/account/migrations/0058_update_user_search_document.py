# Generated by Django 3.2.6 on 2021-12-27 09:47

from django.db import migrations

from ...core.search_tasks import set_user_search_document_values


def update_user_search_document_values(apps, _schema_editor):
    User = apps.get_model("account", "User")
    total_count = User.objects.filter(search_document="").count()
    set_user_search_document_values.delay(total_count, 0)


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0057_user_search_document"),
    ]

    operations = [
        migrations.RunPython(
            update_user_search_document_values, reverse_code=migrations.RunPython.noop
        ),
    ]
