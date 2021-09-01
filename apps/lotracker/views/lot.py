from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lotracker.models import Lot, LotFts
from lotracker.serializers.filter_set import LotFilterValidator, FilterDataSerializer
from lotracker.serializers.lot import LotListSerializer, LotDetailSerializer
from lotracker.utils.pagination import StandardResultsSetPagination
from reference.models import Region, ProductCategory


class LotListAPIView(ListAPIView):
    """
    ### List of Lots with search & filters

    Request example:
    `https://lotracker.rbc-group.uz/api/v1/lots/?q=ручка&region=1&<other_filters>`

    Response example:

        {
            "count": 100,
            "next": "http://127.0.0.1:8000/api/v1/lots/?page=2&q=ручка&region=1",
            "previous": null,
            "results": [
                {
                    "id": 452,
                    "external_id": 5113311,
                    "name": "Сальниковая набивка ХБП",
                    "start_price": 30000000.0,
                    "customer": 152,
                    "current_price": 0.0,
                    "next_price": null,
                    "term_date": "2020-01-30T10:00:00",
                    "requests_count": 0,
                    "site_type": 0,
                    "category__name": "ТМЗ",
                    "region__name": "Наманганская область",
                    "area__name": "г.Наманган",
                    "customer__name": "Норин-Сирдарё ирригация тизимлари хавза бошкармаси хузуридаги насос станциялари
                    ва энергетика бошкармаси"
                }, ...
        }
    """
    serializer_class = LotListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        filters = LotFilterValidator.check(self.request.GET)
        qs = Lot.objects.list(filters).annotate_is_favourite(self.request.user)
        return qs


class LotDetailAPIView(RetrieveAPIView):
    """
    ### Detail information of Lot

    Request example:
    `https://lotracker.rbc-group.uz/api/v1/lots/1/`

    Response example:

        {
            "id": 452,
            "external_id": 5113311,
            "name": "Сальниковая набивка ХБП",
            "start_price": 30000000.0,
            "customer": {
                "id": 152,
                "name": "Норин-Сирдарё ирригация тизимлари хавза бошкармаси хузуридаги насос станциялари...",
                "inn": "200055836-9169153",
                "address": "Наманганская область г.Наманган Наманган вилоят Наманган шахар 4-кичик нохия...",
                "phones": "+998-69-232-6189, 69-232-18-95",
                "bank_account": "100021860144017042402170006"
            },
            "current_price": 0.0,
            "next_price": null,
            "deposit_amount": 900000.0,
            "commission_amount": 44100.0,
            "delivery_days_count": 5,
            "payment_days_count": 10,
            "need_delivery": true,
            "delivery_address": "Наманганская область г.Наманган г.Наманган ул.Галаба 4 мкр.дом.21",
            "term_date": "2020-01-30T10:00:00",
            "conditions": "Поставляемый товар должен быть новый и не бывший в употреблении, а также в заводской...",
            "url": "https://dxarid.uzex.uz/ru/trade/lot/5113311/",
            "requests_count": 0,
            "site_type": 0,
            "category__name": "ТМЗ",
            "region__name": "Наманганская область",
            "area__name": "г.Наманган",
            "lot_items": [
                {
                    "id": 865,
                    "product__name": "Сальниковая набивка ХБП",
                    "description": "Сальниковая набивка ХБП для ремонта насосных агрегатов",
                    "expense_type_text": "Товарно-материальные запасы (кроме бумаги и прочей полиграфической продукции)",
                    "quantity": 1000.0,
                    "unit": "Кг",
                    "start_price": 30000.0,
                    "current_price": null,
                    "next_price": null
                }
            ]
        }
    """
    serializer_class = LotDetailSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Lot.objects.active().annotate_is_favourite(self.request.user).order_by('term_date')


class FilterDataAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get_queryset(self):
        return {
            'regions': Region.objects.all().prefetch_related('areas'),
            'categories': ProductCategory.objects.all().prefetch_related('products'),
        }

    def get(self, request, *args, **kwargs):
        return Response(FilterDataSerializer(instance=self.get_queryset()).data)


class AddToFavouriteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'delete']

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        lot = get_object_or_404(Lot, pk=pk)
        user.favourite_lots.add(lot)
        return Response()

    def delete(self, request, pk, *args, **kwargs):
        user = request.user
        lot = get_object_or_404(Lot, pk=pk)
        user.favourite_lots.remove(lot)
        return Response()


class FavouriteLotsListAPIView(ListAPIView):
    serializer_class = LotListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.request.user.favourite_lots.active().annotate_is_favourite(self.request.user)


class SuggestAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        q = self.request.GET.get('q', '')
        if q and q != '':
            return Response(LotFts.objects.suggestions(q))
        return Response([])
