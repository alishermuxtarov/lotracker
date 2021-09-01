from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from authentication.models import ConfirmationCode, Token, User
from authentication.serializers.signin import SignInSerializer, ConfirmationSerializer
from django.conf import settings

from authentication.serializers.users import UserSerializer
from lotracker.utils.helpers import integers_only
from lotracker.utils.security import AntiPerDayThrottle, AntiPerMinuteThrottle


class SignInView(GenericAPIView):
    """
    ### Creates new user by phone if not exists
    ### Sends SMS with confirmation code
    """
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer
    throttle_key = 'sign_in'

    def get_throttles(self):
        return [AntiPerDayThrottle(), AntiPerMinuteThrottle()] if settings.SEND_CONFIRMATION_SMS else []

    def post(self, request):
        data = SignInSerializer.check(request.data)
        User.objects.sign_in(data.get('phone'), data.get('country'))
        return Response({}, 201)


class ConfirmationView(GenericAPIView):
    """
    ### Check confirmation code sent by sms
    ### Return authentication token and customer info
    """
    permission_classes = (AllowAny,)
    serializer_class = ConfirmationSerializer

    def post(self, request):
        data = self.serializer_class.check(request.data)
        user = get_object_or_404(User, phone=integers_only(data.get('phone')))
        token = Token.objects.create(user=user)
        ConfirmationCode.objects.filter(code=data.get('code'), user=user).update(is_used=True)
        return Response({'token': token.key, 'user': UserSerializer(user).data})
