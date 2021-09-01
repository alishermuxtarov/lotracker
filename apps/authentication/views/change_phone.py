from authentication.models import ConfirmationCode, User
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.serializers.change_phone import ChangePhoneSerializer, ConfirmChangePhoneSerializer
from django.conf import settings
from lotracker.utils.security import AntiPerDayThrottle, AntiPerMinuteThrottle


class ChangePhoneView(APIView):
    throttle_key = 'change_phone'

    def get_throttles(self):
        return [AntiPerDayThrottle(), AntiPerMinuteThrottle()] if settings.SEND_CONFIRMATION_SMS else []

    def post(self, request):
        data = ChangePhoneSerializer.check(request.data)
        confirmation = ConfirmationCode.objects.create(
            type=ConfirmationCode.CHANGE_PHONE,
            phone=data.get('phone'),
            user=self.request.user
        )
        confirmation.send()
        return Response(data)


class ConfirmChangePhoneView(APIView):
    def post(self, request):
        data = ConfirmChangePhoneSerializer.check(request.data)
        confirm = data.pop('confirm')
        User.objects.filter(pk=confirm.user.id).update(phone=data['phone'])
        return Response(data)
