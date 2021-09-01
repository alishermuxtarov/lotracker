from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from reference.models import Product
from reference.serializers import ProductSerializer


class ProductListAPIView(ListAPIView):
    """
    ### List of products with search & filter

    Request example:
    `https://lotracker.rbc-group.uz/api/v1/products/?category=1&q=Сер`

    Response example:

        [
            {
                "id": 1050,
                "name": "Сервиз"
            },
            {
                "id": 355,
                "name": "Сердечко (для замок)"
            }
        ]

    """
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    queryset = Product.objects.all()
    search_fields = ('name',)
    filterset_fields = ('category',)

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)[:10]
