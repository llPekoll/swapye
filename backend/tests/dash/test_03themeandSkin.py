import uuid
from http.cookies import SimpleCookie

from django.test import TestCase

from authie.models import UserAccount


class GameSkinCase(TestCase):
    databases = "__all__"

    def setup(self):
        # test fail
        self.client.cookies = SimpleCookie({"session": uuid.uuid4()})
        response = self.client.get("/games")
        self.assertTrue(response.status_code, 404)
        # then do good
        user = UserAccount.objects.create(
            email="Jose@martins.com",
            password="m des mans",
        )
        self.client.cookies = SimpleCookie({"session": user.uuid})

    def test_03_get_fail(self):
        response = self.client.get("/gametypesnskins/")
        self.assertTrue(response.status_code, 200)
