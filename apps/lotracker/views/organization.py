from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from lotracker.serializers.organization import OrganizationDetailSerializer
from lotracker.utils.pagination import StandardResultsSetPagination
from reference.models import Organization
from reference.serializers import OrganizationSerializer


class OrganizationListAPIView(ListAPIView):
    """
    ### List of organizations

    Request example:
    `https://lotracker.rbc-group.uz/api/v1/organizations/`

    Response example:

        [
            {
                "id": 50,
                "name": "\"Agrobank\" ATB",
                "inn": "207243390",
                "address": "г.Ташкент, Чиланзарский р-он, ул. Мукими 43",
                "phones": "(+998) +998-91-164-3636",
                "bank_account": "19909000200001140907"
            }, ...
        ]

    """
    serializer_class = OrganizationSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    queryset = Organization.objects.active()
    search_fields = ('name', 'inn')

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)[:10]


class OrganizationDetailAPIView(RetrieveAPIView):
    """
    ### Detail information of Lot

    Request example:
    `https://lotracker.rbc-group.uz/api/v1/organizations/1/`

    Response example:

        {
            "id": 50,
            "name": "\"Agrobank\" ATB",
            "inn": "207243390",
            "address": "г.Ташкент, Чиланзарский р-он, ул. Мукими 43",
            "phones": "(+998) +998-91-164-3636",
            "bank_account": "19909000200001140907",
            "lots": [
                {
                    "id": 271,
                    "external_id": 1235283,
                    "name": "Ковровая дорожка",
                    "start_price": 31648248.0,
                    "customer": 50,
                    "current_price": 0.0,
                    "next_price": null,
                    "term_date": "2020-02-05T10:08:20",
                    "requests_count": 0,
                    "site_type": 1,
                    "is_expired": false,
                    "category__name": "ТМЗ",
                    "region__name": "г.Ташкент",
                    "area__name": "Чиланзарский р-он",
                    "customer__name": "\"Agrobank\" ATB"
                }, ...
            ]
        }

    """
    serializer_class = OrganizationDetailSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    queryset = Organization.objects.active()
