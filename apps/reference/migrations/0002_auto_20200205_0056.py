# Generated by Django 2.2.9 on 2020-02-05 00:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name'], 'verbose_name': 'Организация', 'verbose_name_plural': 'Организации'},
        ),
    ]