import time
from datetime import date

from django.db.backends.mysql.features import DatabaseFeatures
from django.db.backends.mysql.validation import DatabaseValidation
from django.db import models, OperationalError


def check(*args, **kwargs):
    return []


setattr(DatabaseFeatures, 'is_sql_auto_is_null_enabled', None)
DatabaseValidation.check = check


class FTSManager(models.Manager):
    SUG_KEY = ['suggest', 'distance', 'docs']

    def get_queryset(self):
        try:
            qs = super().get_queryset()
            qs = qs.using('fts')
            return qs
        except OperationalError:
            pass

    @staticmethod
    def clean_kwargs(kwargs):
        new_kwargs = kwargs.copy()
        for k, v in kwargs.items():
            if v is None:
                new_kwargs.pop(k)
        return new_kwargs

    def create_record(self, **kwargs):
        try:
            self.create(**self.clean_kwargs(kwargs))
        except OperationalError:
            pass

    def update_record(self, **kwargs):
        try:
            self.delete_record(kwargs.get('id'))
            self.create_record(**kwargs)
        except OperationalError:
            pass

    def search(self, **filters):
        result = self._search(**filters)
        if not result and 'word' in filters.keys():
            suggest = self.suggestions(filters.pop('word'))
            if suggest:
                result = self._search(word=suggest[0]['suggest'], **filters)
        return result

    def _search(self, **filters):
        # todo: prevent SQL injection
        try:
            sql = "SELECT id FROM {} WHERE ".format(self.model._meta.db_table)

            if filters.get('word'):
                sql += "MATCH('{}') ".format(filters.pop('word'))
            if filters.get('pk_gt') is not None:
                sql += ' AND id > {}'.format(filters.pop('pk_gt'))

            if filters:
                for k, v in filters.items():
                    s = '='

                    if isinstance(v, models.Model):
                        v = getattr(v, 'pk')
                        k += '_id'

                    if isinstance(v, date):
                        v = time.mktime(v.timetuple())

                    if k.endswith('_from'):
                        k = k.replace('_from', '')
                        s = '>='
                    elif k.endswith('_to'):
                        k = k.replace('_to', '')
                        s = '<='

                    sql += ' AND {} {} {} '.format(k, s, v)
            if filters.get('pk') is not None:
                sql += ' AND id = {}'.format(filters.get('pk'))
            sql += 'LIMIT 1000;'
            sql = sql.replace('WHERE  AND', 'WHERE')
            qs = self.raw(sql, using='fts')
            return [i.pk for i in qs]
        except OperationalError:
            return []

    def suggestions(self, word):
        from django.db import connections

        with connections['fts'].cursor() as cursor:
            cursor.execute(
                "CALL QSUGGEST('{}', '{}')".format(word, self.model._meta.db_table))
            results = cursor.fetchall()
            return [dict(zip(self.SUG_KEY, r)) for r in results]

    def delete_record(self, pk):
        from django.db import connections

        try:
            with connections['fts'].cursor() as cursor:
                sql = "DELETE FROM `{}` WHERE `id` = {}".format(
                    self.model._meta.db_table, pk)
                cursor.execute(sql)
                return cursor.fetchone()
        except OperationalError:
            pass

    def get_record_by_id(self, pk):
        from django.db import connections

        try:
            with connections['fts'].cursor() as cursor:
                sql = "SELECT id FROM `{}` WHERE `id` = {}".format(
                    self.model._meta.db_table, pk)
                cursor.execute(sql)
                return cursor.fetchone()
        except OperationalError:
            pass
