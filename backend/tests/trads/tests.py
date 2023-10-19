from django.test import TestCase, TransactionTestCase


class TradTest(TestCase):
    databases = "__all__"

    def test_trad_view(self):
        resp = self.client.get("/trads/fr/home")
        self.assertEqual(resp.status_code, 200)
