from django.urls import path

from authentication.views.signin import SignInView, ConfirmationView
from authentication.views.change_phone import ChangePhoneView, ConfirmChangePhoneView

urlpatterns = [
    path('signin/', SignInView.as_view(), name='signin'),
    path('confirm/', ConfirmationView.as_view(), name='confirm'),
    path('change_phone/', ChangePhoneView.as_view(), name='change-phone'),
    path('change_phone/confirm/', ConfirmChangePhoneView.as_view(), name='confirm-change-form')
]
