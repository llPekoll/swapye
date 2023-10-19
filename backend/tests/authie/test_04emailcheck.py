import json
import uuid

from django.test import TestCase

from authie.models import UserAccount


class EmailCheckTestCase(TestCase):
    databases = "__all__"

    def test_email_check_email_missing(self):

        payload = {"emailllllll": "willmase"}
        response = self.client.post(
            "auth/email_checker",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertTrue(response.status_code, 422)

    def test_email_check_user_already_in_base(self):
        user = UserAccount.objects.create(
            email="Jose@martins.com",
            password="m des mans",
        )
        payload = {"email": user.email}
        response = self.client.post(
            "auth/email_checker",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertTrue(response.status_code, 409)

    def test_email_check(self):
        UserAccount.objects.create(
            email="Jose@martins.com",
            password="m des mans",
        )
        payload = {"email": "willmase"}
        response = self.client.post(
            "auth/email_checker",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertTrue(response.status_code, 200)
