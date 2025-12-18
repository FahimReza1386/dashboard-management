# Django Imports
from django.urls import reverse_lazy

# Third-Party imports
from rest_framework.test import APITestCase
from rest_framework import status

# Locale Imports
from accounts.factories import UserFactory


class AccountsTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(
            is_superuser=True, is_active=True, is_verified=True, type=1
        )  # 1 is superuser

    def test_api_profiles(self):
        login_url = reverse_lazy("accounts-api:login")
        login_data = {"email": self.user.email, "password": "defaultpassword"}
        response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(reverse_lazy("accounts-api:profile"),
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_users(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse_lazy("accounts-api:users"),
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
