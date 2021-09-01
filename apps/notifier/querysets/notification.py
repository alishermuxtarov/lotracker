from django.db.models import QuerySet
from django.utils import timezone


class NotificationQuerySet(QuerySet):
    def unread(self, recipient_id):
        return self.filter(recipient=recipient_id, is_read=False)

    def unread_count(self, recipient_id):
        return self.unread(recipient_id).count()

    def mark_as_read(self, recipient_id):
        return self.unread(recipient_id).update(is_read=True, read_at=timezone.now())

    def clean_deleted_objects_notifications(self):
        for notification in self.filter(
                action_object_content_type__isnull=False, action_object_object_id__isnull=False):
            model_class = notification.action_object_content_type.model_class()
            if not model_class.objects.filter(pk=notification.action_object_object_id).exists():
                notification.delete()
