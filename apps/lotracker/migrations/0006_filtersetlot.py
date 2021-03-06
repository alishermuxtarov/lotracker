# Generated by Django 2.2.9 on 2020-02-06 20:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lotracker', '0005_auto_20200205_0056'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilterSetLot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False, verbose_name='Прочитано?')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время создания')),
                ('filter_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lots', to='lotracker.FilterSet', verbose_name='Сохраненный набор фильтров')),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_sets_lots', to='lotracker.Lot', verbose_name='Лот')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_sets_lots', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Найденные лоты сохраненных фильтров',
                'verbose_name_plural': 'Найденные лоты сохраненных фильтров',
                'db_table': 'lotracker_filter_sets_lots',
                'ordering': ['-pk'],
            },
        ),
    ]
