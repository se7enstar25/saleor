# Generated by Django 2.0.8 on 2018-09-13 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("menu", "0008_menu_json_content_new")]

    operations = [migrations.RemoveField(model_name="menu", name="json_content")]
