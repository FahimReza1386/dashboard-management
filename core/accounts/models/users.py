# Django Imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from phonenumber_field.modelfields import PhoneNumberField

# Locale Imports
from utils.models.datetime import AbstractDateTimeModel
from accounts.managers.user_manager import UserManager
from accounts.validations.validations import is_valid_iranian_national_code

class Users(AbstractDateTimeModel, AbstractBaseUser, PermissionsMixin):
    class UserTypeModel(models.IntegerChoices):
        superuser = 1, _("SuperUser")
        customer = 2, _("Customer")
        admin = 3, _("Admin")

    username = None
    email = models.EmailField(
        unique=True,
        verbose_name=_("Email Address"),
    )
    first_name = models.CharField(
        max_length=30,
        verbose_name=_("First Name"),
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name=_("Last Name"),
    )
    national_code = models.CharField(
        max_length=10,
        unique=True,
        validators=[is_valid_iranian_national_code],
        verbose_name=_("National Code"),
    )
    phone_number = PhoneNumberField(
        unique=True,
        verbose_name=_("Phone Number"),
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_("Active Status"),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("Staff Status"),
    )
    is_superuser = models.BooleanField(
        default=False, verbose_name=_("SuperUser Status")
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_("Verified Status")
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        verbose_name=_("Avatar"),
    )
    type = models.IntegerField(
        choices=UserTypeModel.choices,
        default=UserTypeModel.customer.value,
        verbose_name=_("User Type"),
    )

    REQUIRED_FIELDS = ["national_code", "phone_number"]
    USERNAME_FIELD = "email"
    objects = UserManager()

    class Meta:
        verbose_name = _("Users")
        verbose_name_plural = _("Users")
        ordering = ["-id"]

    def __str__(self):
        return f"{self.email}"
