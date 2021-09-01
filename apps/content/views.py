from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from lotracker.utils.pagination import StandardResultsSetPagination
from content.serializers import ContentSerializer
from content.models import Content


class ContentListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ContentSerializer
    pagination_class = StandardResultsSetPagination
    ordering = ('-created_at',)
    queryset = Content.objects.all()


class ContentDetailAPIView(RetrieveAPIView):
    serializer_class = ContentSerializer
    queryset = Content.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'slug'
