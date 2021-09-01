from django.urls import path

from content.views import ContentListView, ContentDetailAPIView

urlpatterns = [
    # path('', ContentListView.as_view(), name='list'),
    path('<slug:slug>/', ContentDetailAPIView.as_view(), name='details'),
]
