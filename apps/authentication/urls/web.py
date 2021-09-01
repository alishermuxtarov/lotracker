from django.urls import path

from authentication.views.signin import SignInView, ConfirmationView

urlpatterns = [
    path('signin/', SignInView.as_view(), name='signin'),
    path('confirm/', ConfirmationView.as_view(), name='confirm'),
]
