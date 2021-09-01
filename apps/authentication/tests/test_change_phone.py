from authentication.models import ConfirmationCode, User
from authentication.tests.constants import USER_TOKEN
from django.urls import reverse
from django.test import override_settings

from lotracker.utils.base_test import BaseTestCase
from lotracker.utils.helpers import integers_only


class ChangePhoneTest(BaseTestCase):
    fixtures = ('users_and_tokens', )

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + USER_TOKEN)

    def test_change_phone(self):
        phone = '+998901111111'
        url = reverse('authentication:change-phone')
        response = self.client.post(url, {'phone': phone})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)

        confirm = ConfirmationCode.objects.filter(phone=integers_only(phone)).first()
        url = reverse('authentication:confirm-change-form')
        response = self.client.post(url, {'phone': phone, 'code': confirm.code})
        self.assertEqual(response.status_code, 200)

        data = {'phone': phone, 'code': 12345532}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['code'], ['Неверный код подтверждения'])

    @override_settings(SEND_CONFIRMATION_SMS=False)
    def test_phone_exists(self):
        phone = '+998913333333'
        url = reverse('authentication:change-phone')
        response = self.client.post(url, {'phone': phone})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['phone'], ['Пользователь с таким номером уже существует.'])
