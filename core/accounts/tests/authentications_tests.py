# Django Imports
from django.urls import reverse_lazy
from django.test import override_settings
from django.core import mail
import re

# Third-Party imports
from rest_framework.test import APITestCase
from rest_framework import status

# Locale Imports
from accounts.factories import UserFactory


class AuthenticationsTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(
            is_superuser=True,
            is_active=True,
            is_verified=True
        )

    def test_api_register(self):
        register_url = reverse_lazy("accounts-api:user-register")
        register_data = {
            "email": "FahimTest@gmail.com",
            "password": "FahimTest123",
            "password_confirm": "FahimTest123",
            "national_code": "2503201212",
            "phone_number": "09172188787",
        }
        response = self.client.post(register_url, register_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], "FahimTest@gmail.com")

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
    )
    def test_api_register_verify(self):
        register_url = reverse_lazy("accounts-api:user-register")
        register_data = {
            "email": "VerifyTest@gmail.com",
            "password": "VerifyTest123",
            "password_confirm": "VerifyTest123",
            "first_name": "Verify",
            "last_name": "Test",
            "national_code": "1234567890",
            "phone_number": "+989123456789",
        }
        response = self.client.post(register_url, register_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn("VerifyTest@gmail.com", email.to)

        href_pattern = r'href="([^"]*)"'
        matches = re.findall(href_pattern, email.body)
        self.assertTrue(matches)
        verify_url = matches[0]

        response = self.client.get(verify_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("حساب شما تایید شد", response.data["msg"])

    def test_api_login(self):
        login_url = reverse_lazy("accounts-api:login")
        login_data = {"email": self.user.email, "password": "defaultpassword"}
        response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_refresh(self):
        login_url = reverse_lazy("accounts-api:login")
        login_data = {"email": self.user.email, "password": "defaultpassword"}
        response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["refresh"]

        refresh_url = reverse_lazy("accounts-api:token-refresh")
        refresh_data = {"refresh": token}
        response = self.client.post(refresh_url, refresh_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_verify(self):
        login_url = reverse_lazy("accounts-api:login")
        login_data = {"email": self.user.email, "password": "defaultpassword"}
        response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["access"]

        verify_url = reverse_lazy("accounts-api:token-verify")
        verify_data = {"token": token}
        response = self.client.post(verify_url, verify_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
