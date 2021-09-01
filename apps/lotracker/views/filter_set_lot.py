from datetime import datetime

from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lotracker.models import FilterSetLot
from lotracker.serializers.filter_set_lot import FilterSetLotSerializer
from lotracker.utils.pagination import StandardResultsSetPagination


class FilterSetLotListAPIView(ListAPIView):
    """
    ### List of lots found for saved filters

    Request example:
    `https://lotracker.rbc-group.uz/api/v1/filter_sets_lots/`

    Response example:


    """
    serializer_class = FilterSetLotSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        FilterSetLot.objects.filter(user=self.request.user, is_displayed=False).update(is_displayed=True)
        return FilterSetLot.objects.filter(
            user=self.request.user,
            lot__is_expired=False,
            lot__term_date__gt=datetime.now()
        ).select_related('lot', 'lot__region', 'lot__area', 'lot__category', 'lot__customer', 'filter_set')


class MarkAsReadView(APIView):
    """
    get:

    ### Mark as read filter_set_lot

    Request example:
    `https://lotracker.rbc-group.uz/api/v1/filter_sets_lots/<filter_set_lot_id>/mark_as_read/`

    """
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, pk, *args, **kwargs):
        filter_set_lot = get_object_or_404(FilterSetLot, user=request.user, pk=pk)
        filter_set_lot.is_read = True
        filter_set_lot.save()
        return Response()


class MarkAllAsReadView(APIView):
    """
    get:

    ### Mark as read all filter_set_lot records

    Request example:
    `https://lotracker.rbc-group.uz/api/v1/filter_sets_lots/mark_as_read/`

    """
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        FilterSetLot.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response()
