from django.apps import AppConfig


class AggregatorConfig(AppConfig):
    name = 'lotracker'
    verbose_name = 'Агрегатор'

    def ready(self):
        import lotracker.signals

