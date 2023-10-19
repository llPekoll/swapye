import json
import uuid
from http.cookies import SimpleCookie

from django.test import TestCase

from authie.models import UserAccount, UserPersonalInfo


class PersonalsTestCase(TestCase):
    databases = "__all__"

    def test_get_personals_fail(self):
        self.client.cookies = SimpleCookie({"session": uuid.uuid4()})
        response = self.client.get("personals")
        self.assertTrue(response.status_code, 404)

    def test_get_personals_empty(self):
        user = UserAccount.objects.create(
            email="Jose@martins.com",
            password="m des mans",
        )
        self.client.cookies = SimpleCookie({"session": str(user.uuid)})
        response = self.client.get("personals")
        self.assertTrue(response.status_code, 200)

    def test_get_personals_full(self):
        user = UserAccount.objects.create(
            email="Jose@martins.com",
            password="m des mans",
        )
        UserPersonalInfo.objects.create(
            owner=user,
            name="jose",
            conact_email="jose@martins.com",
            company_name="jose martins",
            rib="jose",
            siret="jose",
            phone="jose",
            address="jose",
            postal=12345,
            city="jose",
        )
        self.client.cookies = SimpleCookie({"session": str(user.uuid)})
        response = self.client.get("personals")
        self.assertTrue(response.status_code, 202)
