# from http.cookies import SimpleCookie

# from django.test import TestCase

# from authie.models import UserAccount
# from dash.models import GameType, Skin
# from games.models import Game, Price


# class GameTestCase(TestCase):
#     databases = "__all__"

#     def setup(self):
#         user = UserAccount.objects.create(
#             email="Jose@martins.com",
#             password="m des mans",
#         )
#         self.client.cookies = SimpleCookie({"session": str(user.uuid)})

#     def test_create(self):
#         self.client.cookies = SimpleCookie({"session": str(user.uuid)})
#         payload = {
#             "name": "first game",
#             "type": "curtain",
#             "skin": "La skin du curtain",
#         }
#         self.client.cookies = SimpleCookie({"session": str(user.uuid)})
#         response = self.client.post(
#             "/games", content_type="application/json", data=payload
#         )
#         game_nb = Game.objects.all().count()
#         self.assertEqual(game_nb, 1)
#         self.assertTrue(response.status_code, 201)

#     def test_delete_game(self):
#         user = UserAccount.objects.create(
#             email="Jose@martins.com",
#             password="m des mans",
#         )
#         game_type = GameType.objects.create()
#         skin = Skin.objects.create(game=game_type)
#         Game.objects.create(
#             owner=user,
#             emblem="mmdSako7",
#             link="santinano",
#             qr_location="no need for more qr",
#             name="tinsmar msj",
#             game_type=game_type,
#             skin=skin,
#         )
#         self.client.cookies = SimpleCookie({"session": str(user.uuid)})
#         response = self.client.delete("/games")
#         game_nb = Game.objects.all().count()
#         self.assertEqual(game_nb, 0)
#         self.assertTrue(response.status_code, 201)

#     def test_create_price(self):
#         user = UserAccount.objects.create(
#             email="Jose@martins.com",
#             password="m des mans",
#         )
#         game_type = GameType.objects.create()
#         skin = Skin.objects.create(game=game_type)
#         game = Game.objects.create(
#             owner=user,
#             emblem="mmdSako7",
#             link="santinano",
#             qr_location="no need for more qr",
#             name="tinsmar msj",
#             game_type=game_type,
#             skin=skin,
#         )
#         payload = {
#             "display_price_name": True,
#             "name": "jose",
#             "img": "img dses mans",
#             "quantity": 120,
#             "offset_price_name": "mt-2",
#             "email_template": 123,
#             "winnableTimeRage1": 10,
#             "winnableTimeRage2": 20,
#             "winnableTimeRage3": 30,
#         }
#         response = self.client.post(
#             f"/dash/{game.emblem}/prices",
#             content_type="application/json",
#             data=payload,
#         )
#         logger.info(response)
#         price_nb = Price.objects.all()
#         self.assertNotEqual(len(price_nb), 0)
#         self.assertTrue(response.status_code, 201)

#     def test_delete_prices(self):
#         user = UserAccount.objects.create(
#             email="Jose@martins.com",
#             password="m des mans",
#         )
#         game_type = GameType.objects.create()
#         skin = Skin.objects.create(game=game_type)
#         game = Game.objects.create(
#             owner=user,
#             emblem="mmdSako7",
#             link="santinano",
#             qr_location="no need for more qr",
#             name="tinsmar msj",
#             game_type=game_type,
#             skin=skin,
#         )
#         price = Price.objects.create(
#             game=game,
#             name="sako",
#             img="mmd",
#             number=1234,
#             display_price_name=True,
#             offset_price_name="mt-4",
#             email_template="123123",
#         )
#         response = self.client.delete(f"/dash/{game.emblem}/prices/{price.id}")
#         price_nb = Price.objects.all().count()
#         self.assertEqual(price_nb, 0)
#         self.assertTrue(response.status_code, 204)
