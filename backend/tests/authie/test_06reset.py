import json
import uuid

from django.test import TestCase

from authie.models import Reset, UserAccount


class ResetTestCase(TestCase):
    databases = "__all__"

    def test_reset_payload(self):
        payload = {"tokeennenen": "Jose@martins.com"}
        response = self.client.post(
            "auth/reset", data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 422)

    def test_login_fail_missing_token(self):
        user = UserAccount.objects.create(email="jis@asdf.com", password="only django")
        token = Reset.objects.create(email=user.email, token="willmase")
        payload = {"token": "sako"}
        response = self.client.post(
            "auth/reset", data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 404)

    def test_token(self):
        user = UserAccount.objects.create(email="jis@asdf.com", password="only django")
        token = Reset.objects.create(email=user.email, token="willmase")
        payload = {"token": token.token}
        response = self.client.post(
            "auth/reset", data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 404)
