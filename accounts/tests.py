from django.db.models import Model
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AccountTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User: Model = get_user_model()
        cls.credentials = {"username": "testuser", "password": "secret"}
        User.objects.create_user(**cls.credentials)

    def test_auth(self):
        fail_response = self.client.post(
            reverse("accounts:obtain_token"), {"username": "t", "password": "1"}
        )
        success_response = self.client.post(
            reverse("accounts:obtain_token"), self.credentials
        )

        auth_response = self.client.get(
            reverse("kilterboard:index"),
            HTTP_AUTHORIZATION=f"Bearer {success_response.data['access']}",
        )
        not_auth_response = self.client.get(
            reverse("kilterboard:index"), HTTP_AUTHORIZATION="Bearer test"
        )

        self.assertEqual(fail_response.data["access"], "None")
        self.assertNotEqual(success_response.data["access"], "None")
        self.assertEqual(auth_response.status_code, 200)
        self.assertEqual(not_auth_response.status_code, 401)

    def test_refresh(self):
        response = self.client.post(reverse("accounts:obtain_token"), self.credentials)
        response = self.client.post(
            reverse("accounts:refresh_token"), {"refresh": response.data["refresh"]}
        )
        response = self.client.get(
            reverse("kilterboard:index"),
            HTTP_AUTHORIZATION=f"Bearer {response.data['access']}",
        )

        self.assertEqual(response.status_code, 200)
