import uuid
from http.cookies import SimpleCookie

from django.test import TestCase

from authie.models import UserAccount
from games.models import Game


class GameDetailsCase(TestCase):
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
        payload = {
            "name": "first game",
            "type": "1",
            "skin": "1",
        }
        response = self.client.post(
            "/games", content_type="application/json", data=payload
        )
        res = response.json()
        self.game_id = res["game_id"]
        game_nb = Game.objects.all().count()
        self.assertEqual(game_nb, 1)
        self.assertTrue(response.status_code, 201)

    def test_01_get_fail(self):
        response = self.client.get("/games/rweqr22323233232")
        self.assertTrue(response.status_code, 404)

    def test_02_get_ok(self):
        response = self.client.get(f"/games/{self.game_id}")
        self.assertTrue(response.status_code, 200)

    def test_03_delete_fail(self):
        response = self.client.delete("/games/fsdfasdfasfd")
        self.assertTrue(response.status_code, 404)

    def test_04_delete_ok(self):
        response = self.client.delete(f"/games/{self.game_id}")
        self.assertTrue(response.status_code, 200)
