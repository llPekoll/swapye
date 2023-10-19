import uuid
from http.cookies import SimpleCookie

from django.test import TestCase

from authie.models import UserAccount
from games.models import Game


class GameListCase(TestCase):
    databases = "__all__"

    def setUp(self):
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

    def test_01_getList(self):
        response = self.client.get("/games")
        self.assertTrue(response.status_code, 200)

    def test_02_create(self):
        payload = {
            "name": "first game",
            "type": "1",
            "skin": "1",
        }
        response = self.client.post(
            "/games", content_type="application/json", data=payload
        )
        game_nb = Game.objects.all().count()
        self.assertEqual(game_nb, 1)
        self.assertTrue(response.status_code, 201)
