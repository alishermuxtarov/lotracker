# Generated by Django 2.2.9 on 2020-02-07 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_favourite_lots'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_uid',
            field=models.BigIntegerField(blank=True, editable=False, null=True),
        ),
    ]