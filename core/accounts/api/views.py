# Django Imports
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.utils.translation import gettext as _

# Third-Party Imports
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    GenericAPIView,
    ListAPIView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
    TokenRefreshView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from mail_templated import send_mail
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt
from datetime import datetime, timedelta
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Locale Imports
from accounts.api.serializers import (
    ProfileApiSerializers,
    RegisterApiSerializer,
    VerifyApiSerializer,
    UsersListApiSerializer,
)
from accounts.models import Users
from accounts.api.accounts_pagination import AccountsPagination

"""

    Users Management Views

"""


class ProfilesApiView(RetrieveAPIView):
    serializer_class = ProfileApiSerializers
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user


class UsersApiView(ListAPIView):
    serializer_class = UsersListApiSerializer
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["email", "first_name",
                        "last_name", "is_active",
                        "is_verified"]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = ["id", "nationa_code"]
    pagination_class = AccountsPagination


class RegisterApiView(CreateAPIView):
    serializer_class = RegisterApiSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            email = serializer.validated_data["email"]

            data = {
                "email": email,
                "msg": _("Hello dear user, your account verification link has been sent to your email."
"You can activate your account only up to 5 hours after this link is sent."),
            }

            user = get_object_or_404(Users, email=email)

            payload = {
                "email": email,
                "user_id": user.id,
                "exp": datetime.utcnow() + timedelta(hours=5),
                "iat": datetime.utcnow(),
            }

            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
            verify_url = self.request.build_absolute_uri(
                reverse("accounts-api:user-verify", args=[token])
            )

            send_mail(
                "email/email-auth.tpl",
                {"url": verify_url},
                "FahimWeb.ir@gmail.com",
                [email],
            )
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterVerifyView(GenericAPIView):
    serializer_class = VerifyApiSerializer

    def get(self, request, token, *args, **kwargs):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms="HS256")
            user_id = payload.get("user_id")
            user = get_object_or_404(Users, pk=user_id)
            if user:
                user.is_active = True
                user.is_verified = True
                user.is_staff = True
                user.save()

                data = {
                    "email": user.email,
                    "msg": _("Dear user, I am glad that you have chosen our collection."
                            "Your account has been verified."),
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {"msg": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except ExpiredSignatureError:
            return Response({"msg": "The verification link has expired."})
        except (InvalidTokenError, Exception):
            return Response({"msg": "The verification link is invalid."})


class LoginApiView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.user
        login(request, user)
        
        return Response(serializer.validated_data, status=200)

class TokenRefreshApiView(TokenRefreshView):
    pass


class TokenVerifyApiView(TokenVerifyView):
    pass
