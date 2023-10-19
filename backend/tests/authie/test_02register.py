import json
import uuid

from django.test import TestCase

from authie.models import UserAccount


class RegisterUserTestCase(TestCase):
    databases = "__all__"

    def test_register(self):
        payload = {"email": "jism", "password": "sako"}
        response = self.client.post(
            "auth/register", data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 201)

    def test_register_fail_duplicate(self):
        payload = {"emai": "jose", "password": "martins"}
        response = self.client.post(
            "auth/register", data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 422)

    def test_register_fail_pass_missing(self):
        payload = {"emil": "jose"}
        response = self.client.post(
            "auth/register", data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 422)
