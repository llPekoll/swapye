import uuid

from django.test import TestCase

from authie.models import UserAccount


class FetchUserTestCase(TestCase):
    databases = "__all__"

    def test_fecht_user(self):
        user = UserAccount.objects.create(email="jose", password="sako")
        response = self.client.get(f"auth/user/{user.uuid}")
        self.assertTrue(response.status_code, 201)

    def test_fecht_user_missing(self):
        response = self.client.get(f"auth/user/{str(uuid.uuid4())}")
        self.assertTrue(response.status_code, 404)
