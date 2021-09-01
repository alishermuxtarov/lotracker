from django.urls import reverse

from lotracker.utils.base_test import BaseTestCase


class ConfirmationTest(BaseTestCase):
    fixtures = ('users_and_tokens.yaml', 'confirm.yaml')

    def test_confirmation(self):
        data = {'code': '1894', 'phone': '998911234567'}
        response = self.client.post(reverse('authentication:confirm'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['id'], 1)

        data = {'code': '9584', 'phone': '998913333333'}
        response = self.client.post(reverse('authentication:confirm'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['code'], ['Неверный код подтверждения'])
