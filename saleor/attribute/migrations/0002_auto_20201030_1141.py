# Generated by Django 3.1 on 2020-10-30 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("attribute", "0001_initial"),
        ("product", "0137_drop_attribute_models"),
    ]

    operations = [
        migrations.AlterModelTable(name="assignedpageattribute", table=None,),
        migrations.AlterModelTable(name="assignedproductattribute", table=None,),
        migrations.AlterModelTable(name="assignedvariantattribute", table=None,),
        migrations.AlterModelTable(name="attribute", table=None,),
        migrations.AlterModelTable(name="attributepage", table=None,),
        migrations.AlterModelTable(name="attributeproduct", table=None,),
        migrations.AlterModelTable(name="attributetranslation", table=None,),
        migrations.AlterModelTable(name="attributevalue", table=None,),
        migrations.AlterModelTable(name="attributevaluetranslation", table=None,),
        migrations.AlterModelTable(name="attributevariant", table=None,),
    ]
