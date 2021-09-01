from django.db.models import Count, Q
from django.db.models.functions import Now
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from lotracker.models import FilterSet
from lotracker.serializers.filter_set import FilterSetSerializer, FilterSetListSerializer


class FilterSetListCreateAPIView(ListAPIView, CreateAPIView):
    """
    ### List of saved filters

    Request example:
    `https://lotracker.rbc-group.uz/api/v1/filter_sets/`

    Response example:

        [
            {
                "id": 11,
                "name": "Ручка",
                "q": "Ручка",
                "hot_lots": null,
                "without_request": null,
                "term_date_from": null,
                "term_date_to": null,
                "price_from": null,
                "price_to": null,
                "region": null,
                "area": null,
                "organization": null,
                "product_category": null,
                "product": null,
                "site_type": null
            }
        ]
    """
    serializer_class = FilterSetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return FilterSet.objects.filter(user=self.request.user).annotate(
            lots_count=Count('lots', Q(lots__lot__term_date__gte=Now()))
        ).select_related(
            'region', 'area', 'organization', 'product_category', 'product'
        )

    def get_serializer_class(self):
        if getattr(self.request, 'method', None) == 'GET':
            return FilterSetListSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FilterSetUpdateDeleteAPIView(DestroyAPIView, UpdateAPIView, RetrieveAPIView):
    """
    delete:

    ### Deleting filter set

    Request example:
    `DELETE https://lotracker.rbc-group.uz/api/v1/filter_sets/1/`

    put:

    ### Update filter set
    `PATCH https://lotracker.rbc-group.uz/api/v1/filter_sets/1/`

        [
            {
                "name": "Ручка",
                "q": "Ручка",
                "hot_lots": null,
                "without_request": null,
                "term_date_from": null,
                "term_date_to": null,
                "price_from": null,
                "price_to": null,
                "region": null,
                "area": null,
                "organization": 1,
                "product_category": null,
                "product": null,
                "site_type": null
            }
        ]

    patch:

    ### Partial update filter set
    `PATCH https://lotracker.rbc-group.uz/api/v1/filter_sets/1/`

        [
            {
                "name": "Ручка",
                "q": "Ручка и карандаши",
                "without_request": true
            }
        ]
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FilterSetSerializer

    def get_queryset(self):
        return FilterSet.objects.filter(user=self.request.user)
