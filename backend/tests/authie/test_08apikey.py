import json
import uuid
from http.cookies import SimpleCookie

from django.test import TestCase

from authie.models import MailingInfo, UserAccount


class APIkeyTestCase(TestCase):
    databases = "__all__"

    def test_get_apikey_fail(self):
        self.client.cookies = SimpleCookie({"session": uuid.uuid4()})
        response = self.client.get("apikey")
        self.assertTrue(response.status_code, 404)

    def test_get_apikey_empty(self):
        user = UserAccount.objects.create(
            email="Jose@martins.com",
            password="m des mans",
        )
        self.client.cookies = SimpleCookie({"session": str(user.uuid)})
        response = self.client.get("apikey")
        self.assertTrue(response.status_code, 200)

    def test_get_apikey_full(self):
        user = UserAccount.objects.create(
            email="Jose@martins.com",
            password="m des mans",
        )
        MailingInfo.objects.create(
            owner=user,
            provider="MailJet",
            apikey="jose@martins.com",
            apipass="jose martins",
            email="jose",
            display_name="jose",
        )
        self.client.cookies = SimpleCookie({"session": str(user.uuid)})
        response = self.client.get("apikey")
        self.assertTrue(response.status_code, 202)

    def test_post_apikey_full(self):
        user = UserAccount.objects.create(
            email="Jose@martins.com",
            password="m des mans",
        )
        payload = {
            "provider": "jose",
            "apikey": "jose",
            "apipass": "jose",
            "email": 12345,
            "display_name": "jose",
        }
        self.client.cookies = SimpleCookie({"session": str(user.uuid)})
        response = self.client.post(
            "apikey", data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 202)
