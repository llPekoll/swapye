import json
import uuid

from django.test import TestCase

from authie.models import UserAccount


class ForgotTestCase(TestCase):
    databases = "__all__"

    def test_login_fail_payload(self):
        payload = {"emasadfil": "Jose@martins.com"}
        response = self.client.post(
            "auth/forgot", data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 422)

    def test_login_fail_missing_user(self):
        user = UserAccount.objects.create(
            email="Jose@martins.com",
            password="willmase",
        )
        payload = {"email": user.email}
        response = self.client.post(
            "auth/forgot", data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 404)

    def test_settings_apikey(self):
        payload = {"email": "yoyo.mepa@gmail.com"}
        response = self.client.post(
            "auth/forgot", data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 200)
