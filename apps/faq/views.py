from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from lotracker.utils.pagination import StandardResultsSetPagination
from faq.serializers import FaqSerializer
from faq.models import Faq


class FaqListView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = FaqSerializer
    permission_classes = [AllowAny]
    queryset = Faq.objects.all()
    ordering = ('-created_at',)
