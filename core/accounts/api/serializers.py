# Django Imports
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

# Third-Party Imports
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Locale Imports
from accounts.models import Users


class ProfileApiSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "national_code",
            "type",
        )


class RegisterApiSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = (
            "email",
            "password",
            "password_confirm",
            "national_code",
            "phone_number",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs["password"]
        password_confirm = attrs["password_confirm"]

        if password != password_confirm:
            raise ValidationError(
                _("The password and password confirm must be the same.")
            )

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = Users.objects.create_user(**validated_data)
        return user


class VerifyApiSerializer(serializers.Serializer):
    token = serializers.CharField()


"""
    Management Users Serializer
"""


class UsersListApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "is_verified",
            "is_active",
            "is_superuser",
            "type",
            "created_at",
            "updated_at",
        ]


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields=("email", "password",)
