from django.db import migrations


def assign_access_key(apps, schema):
    vatlayer_configuration = (
        apps.get_model("plugins", "PluginConfiguration")
        .objects.filter(identifier="mirumee.taxes.vatlayer")
        .first()
    )

    if vatlayer_configuration:
        vatlayer_configuration.active = False
        vatlayer_configuration.save()


class Migration(migrations.Migration):

    dependencies = [
        ("plugins", "0003_auto_20200429_0142"),
    ]

    operations = [
        migrations.RunPython(assign_access_key),
    ]
