# Generated by Django 3.0.2 on 2020-01-28 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lotracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='site_type',
            field=models.SmallIntegerField(choices=[(0, 'dxarid'), (1, 'exarid')], db_index=True, default=1),
        ),
    ]
