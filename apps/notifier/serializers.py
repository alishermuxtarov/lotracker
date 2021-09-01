from json import JSONDecodeError
from rest_framework import serializers
from rest_framework.utils import json

from notifier.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, notification):
        try:
            return json.loads(notification.data)
        except JSONDecodeError:
            return None

    class Meta:
        model = Notification
        fields = ('id', 'text', 'level', 'verb', 'is_read', 'data', 'created_at')
