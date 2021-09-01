from django.utils import timezone

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from lotracker.utils.pagination import StandardResultsSetPagination
from notifier.serializers import NotificationSerializer
from notifier.models import Notification


class NotificationListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = StandardResultsSetPagination
    ordering = ('-created_at',)

    def get_queryset(self):
        return Notification.objects.filter(recipient_id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        result = self.list(request, *args, **kwargs)
        self.get_queryset().update(is_read=True, read_at=timezone.now())
        return result


class UnreadNotificationsCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'count': Notification.objects.unread_count(recipient_id=self.request.user.id)})
