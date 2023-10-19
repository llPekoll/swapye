import json

from django.test import TestCase

from authie.models import UserAccount


class LoginTestCase(TestCase):
    databases = "__all__"

    def test_login_fail_serializer(self):
        payload = {"email": "Jose@martins.com"}
        response = self.client.post(
            "auth/login", data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 403)

    def test_login_fail_missing_user(self):
        user = UserAccount.objects.create(
            email="Jose@martins.com",
            password="m des mans",
        )
        payload = {"email": "jar@jargames.com", "password": user.password}
        response = self.client.post(
            "auth/login", data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 404)

    def test_login_wrong_password(self):
        user = UserAccount.objects.create(
            email="Jose@martins.com",
            password="m des mans",
        )
        payload = {"emil": user.email, "password": "jism"}
        response = self.client.post(
            "auth/login", data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 422)

    def test_login(self):
        user = UserAccount.objects.create(
            email="Jose@martins.com",
            password="m des mans",
        )
        payload = {"email": user.email, "password": user.password}
        response = self.client.post(
            "auth/login", data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 200)
