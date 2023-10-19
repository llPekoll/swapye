import json

from django.test import TestCase

from authie.models import UserAccount
from dash.models import GameType, Skin
from games.models import Game, Price


class GameTestCase(TestCase):
    databases = "__all__"

    def create_game(self, game_type, skin):
        user = UserAccount.objects.create(
            email="Jose@martins.com",
            password="m des mans",
        )
        game_type = GameType.objects.create()
        skin = Skin.objects.create(game=game_type)
        game = Game.objects.create(
            owner=user,
            emblem="mmdSako7",
            link="santinano",
            qr_location="no need for more qr",
            name="tinsmar msj",
            game_type=game_type,
            skin=skin,
        )
        return game

    def create_price(self, game):
        price = Price.objects.create(
            game=game,
            name="sako",
            img="mmd",
            number=1234,
            display_price_name=True,
            offset_price_name="mt-4",
            email_template="123123",
        )
        return price

    def add_lead(self, game):
        lead = Lead.objects.create(
            game=game,
            name="sako",
            img="mmd",
            number=1234,
            display_price_name=True,
            offset_price_name="mt-4",
            email_template="123123",
        )
        return lead

    def add_refused_lead(self, game):
        lead = RefusedLead.objects.create(
            game=game,
            name="sako",
            img="mmd",
            number=1234,
            display_price_name=True,
            offset_price_name="mt-4",
            email_template="123123",
        )
        return lead

    def test_play_base_game_skin_base(self):
        game = self.create_game(1, 1)
        response = self.client.get(f"/play/{game.emblem}")
        self.assertTrue(response.status_code, 200)

    def test_get_leads(self):
        pass

    # tester already play today
    # terter just already play
    # tester looser
    def test_add_lead_loser(self):
        game = self.create_game(1, 1)
        self.create_price(game)
        url = "/leads"
        payload = {
            "name": "martins",
            "phone": "0145950168",
            "address": "2 place de la plataneraie",
            "can_reveceive_email": True,
        }
        response = self.client.post(
            url, data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.json()["name"], "sako")

    def test_add_lead(self):
        game = self.create_game(1, 1)
        self.create_price(game)
        url = "/leads"
        payload = {
            "name": "martins",
            "phone": "0145950168",
            "address": "2 place de la plataneraie",
            "can_reveceive_email": True,
        }
        response = self.client.post(
            url, data=json.dumps(payload), content_type="application/json"
        )
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.json()["name"], "sako")
