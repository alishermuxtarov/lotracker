from django.db.models import QuerySet


class OrganizationQuerySet(QuerySet):
    def active(self):
        return self.all()
