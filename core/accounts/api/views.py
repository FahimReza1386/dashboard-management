# Django Imports
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404

# Third-Party Imports
from rest_framework.generics import CreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from mail_templated import send_mail
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt
from datetime import datetime, timedelta

# Locale Imports
from accounts.api.serializers import ProfileApiSerializers, RegisterApiSerializer, VerifyApiSerializer
from accounts.models import Users


class ProfilesApiView(RetrieveAPIView):
    serializer_class=ProfileApiSerializers
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user

class RegisterApiView(CreateAPIView):
    serializer_class=RegisterApiSerializer

    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            email=serializer.validated_data["email"]

            data = {
                "email" : email,
                "msg" : "سلام کاربر گرامی لینک تایید حساب شما به ایمیلتان ارسال شذ تنها تا ۵ پنج ساعت پس از ارسال این لینک میتوانید حساب خود را فعال کنید ."
            }
            
            user= get_object_or_404(Users, email=email)
            
            payload = {
                "email": email,
                "user_id":user.id,
                "exp" : datetime.utcnow() + timedelta(hours=5),
                "iat" : datetime.utcnow()
            }
            
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
            verify_url= self.request.build_absolute_uri(
                reverse("accounts-api:user-verify", args=[token])
            )

            send_mail(
                "email/email-auth.tpl",
                {"url": verify_url},
                'FahimWeb.ir@gmail.com',
                [email]
            )
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterVerifyView(GenericAPIView):
    serializer_class = VerifyApiSerializer
    def get(self, request,token, *args, **kwargs):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user_id = payload.get("user_id")
            user= get_object_or_404(Users, pk=user_id)
            if user:
                user.is_active=True
                user.is_verified=True
                user.is_staff=True
                user.save()
                
                data = {
                    "email" : user.email,
                    "msg" : "کاربر گرامی خوشحالم از اینکه مجموعه مارو انتخاب کردید ، حساب شما تایید شد ."
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response({"msg": "کاربر یافت نشد ."}, status=status.HTTP_404_NOT_FOUND)
        except ExpiredSignatureError:
            return Response({"msg" : "لینک تایید منقضی شده است."})
        except (InvalidTokenError, Exception):
            return Response({"msg" : "لینک تایید نامعتبر است ."})

class LoginApiView(TokenObtainPairView):
    pass

class TokenRefreshApiView(TokenRefreshView):
    pass

class TokenVerifyApiView(TokenVerifyView):
    pass