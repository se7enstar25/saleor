# Generated by Django 3.0.5 on 2020-04-15 06:21

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
import oauthlib.common
from django.db import migrations, models

import saleor.core.utils.json_serializer


def update_contentypes(apps, schema_editor):
    """Update content types.

    We want to have the same content type id, when the model is moved.
    """
    ContentType = apps.get_model("contenttypes", "ContentType")
    db_alias = schema_editor.connection.alias
    # Move the ServiceAccount to app module
    qs = ContentType.objects.using(db_alias).filter(app_label="account", model="app")
    qs.update(app_label="app")

    # Move the ServiceAccountToken to app module
    qs = ContentType.objects.using(db_alias).filter(
        app_label="account", model="apptoken"
    )
    qs.update(app_label="app")


def update_contentypes_reverse(apps, schema_editor):
    """Revert changes in content types."""
    ContentType = apps.get_model("contenttypes", "ContentType")
    db_alias = schema_editor.connection.alias

    qs = ContentType.objects.using(db_alias).filter(app_label="app", model="app")
    qs.update(app_label="account")

    qs = ContentType.objects.using(db_alias).filter(app_label="app", model="apptoken")
    qs.update(app_label="account")


def convert_service_account_permissions_to_app_permissions(apps, schema_editor):
    Permission = apps.get_model("auth", "Permission")
    service_account_permission = Permission.objects.filter(
        codename="manage_service_accounts", content_type__app_label="app"
    ).first()
    if service_account_permission:
        service_account_permission.codename = "manage_apps"
        service_account_permission.name = "Manage apps"
        service_account_permission.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0011_update_proxy_permissions"),
        ("account", "0041_auto_20200416_0107"),
    ]

    state_operations = [
        migrations.CreateModel(
            name="App",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=60)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this app.",
                        related_name="app_set",
                        related_query_name="app",
                        to="auth.Permission",
                    ),
                ),
                (
                    "metadata",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True,
                        default=dict,
                        encoder=saleor.core.utils.json_serializer.CustomJsonEncoder,
                        null=True,
                    ),
                ),
                (
                    "private_metadata",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True,
                        default=dict,
                        encoder=saleor.core.utils.json_serializer.CustomJsonEncoder,
                        null=True,
                    ),
                ),
            ],
            options={
                "db_table": "app_app",
                "permissions": (("manage_apps", "Manage apps"),),
            },
        ),
        migrations.CreateModel(
            name="AppToken",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, default="", max_length=128)),
                (
                    "auth_token",
                    models.CharField(
                        default=oauthlib.common.generate_token,
                        max_length=30,
                        unique=True,
                    ),
                ),
                (
                    "app",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tokens",
                        to="app.App",
                    ),
                ),
            ],
            options={"db_table": "app_apptoken"},
        ),
    ]

    database_operations = [
        migrations.RunPython(update_contentypes, update_contentypes_reverse),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=state_operations, database_operations=database_operations
        ),
        migrations.AlterModelTable(name="app", table=None,),
        migrations.AlterModelTable(name="apptoken", table=None,),
        migrations.RunPython(convert_service_account_permissions_to_app_permissions),
    ]
