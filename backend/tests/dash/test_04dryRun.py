import uuid
from http.cookies import SimpleCookie

from django.test import TestCase

from authie.models import UserAccount
from games.models import Game


class GameDryRunCase(TestCase):
    databases = "__all__"
    emblem = ""

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
        payload = {
            "name": "first game",
            "type": "1",
            "skin": "1",
        }
        response = self.client.post(
            "/games", content_type="application/json", data=payload
        )
        res = response.json()
        self.emblem = res["emblem"]
        game_nb = Game.objects.all().count()
        self.assertEqual(game_nb, 1)
        self.assertTrue(response.status_code, 201)

    def test_04_get_404(self):
        response = self.client.get(f"/dash/mamadousako/dryrun/")
        self.assertTrue(response.status_code, 404)

    def test_04_get_success(self):
        response = self.client.get(f"/dash/{self.emblem}/dryrun/")
        self.assertTrue(response.status_code, 200)

    def test_04_put_404(self):
        payload = {}
        response = self.client.put(
            f"/dash/fasjdnfapsijn/dryrun/",
            content_type="application/json",
            data=payload,
        )
        self.assertTrue(response.status_code, 404)

    def test_04_put_success(self):
        payload = {
            "forceResultWon": True,
            "force_result_lost": True,
            "forceResultCantReplay": True,
            "forceResultCantReplayToday": True,
            "dryRun": True,
        }
        response = self.client.put(
            f"/dash/{self.emblem}/dryrun/",
            content_type="application/json",
            data=payload,
        )
        self.assertTrue(response.status_code, 200)
