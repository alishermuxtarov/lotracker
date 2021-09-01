from django.urls import reverse
from django.test import override_settings

from lotracker.utils.base_test import BaseTestCase


class AuthenticationTest(BaseTestCase):
    fixtures = ('users_and_tokens.yaml',)

    @override_settings(SEND_CONFIRMATION_SMS=False)
    def test_signin_and_confirm(self):
        url = reverse('authentication:signin')

        response = self.client.post(url, {'phone': '998911234567'})
        self.assertEqual(response.status_code, 201)

        response = self.client.post(url, {'phone': '998911234567'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['user'], ['Повторная отправка SMS возможна через 60 секунд'])

        response = self.client.post(url, {'phone': '998913333333'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['user'], ['Пользователь не активен'])

        response = self.client.post(reverse('authentication:confirm'), {'phone': '+998913106622', 'code': '0000'})
        self.assertEqual(response.data['code'], ['Неверный код подтверждения'])
        self.assertEqual(response.status_code, 400)

    @override_settings(SEND_CONFIRMATION_SMS=True)
    def test_security(self):
        url = reverse('authentication:signin')
        data = {'phone': '998911234567'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 429)

    def test_tokens(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token asuwhhwhwhehhedhdhddsjhfgsdf')
        response = self.client.post(reverse('notifier:notifications'))
        self.assertEqual(response.data['detail'], 'Недопустимый токен.')
        self.assertEqual(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION='Token 5e84409f824bae3e5aa03a3efe4313c9')
        response = self.client.post(reverse('notifier:notifications'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Пользователь неактивен или удален.')
