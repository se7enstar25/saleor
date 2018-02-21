# Generated by Django 2.0.2 on 2018-02-20 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(db_index=True, max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('public', 'Public')], default='draft', max_length=255)),
            ],
            options={
                'ordering': ('url',),
            },
        ),
        migrations.CreateModel(
            name='PostAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset', models.FileField(upload_to='page')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='page.Page')),
            ],
        ),
    ]
