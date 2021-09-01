from django.urls import path

from notifier.views import NotificationListView, UnreadNotificationsCountView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('unread_count/', UnreadNotificationsCountView.as_view(), name='unread_count'),
]
