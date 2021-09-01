from django.urls import path

from faq.views import FaqListView

urlpatterns = [
    path('', FaqListView.as_view(), name='faq'),
]
