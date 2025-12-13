# Django Imports
from django.urls import path

# Locale Imports
from . import views

app_name = "accounts-api"

USER_URLS = [
    path("profiles/", views.ProfilesApiView.as_view(), name="profile"),
]

AUTHENTICATIONS_URLS = [
    path("register/", views.RegisterApiView.as_view(), name="user-register"),
    path("register/verify/<str:token>/", views.RegisterVerifyView.as_view(), name="user-verify"),
    path("token/login/", views.LoginApiView.as_view(), name="login"),
    path("token/refresh/", views.TokenRefreshApiView.as_view(), name="token-refresh"),
    path("token/verify/", views.TokenVerifyApiView.as_view(), name="token-verify")
]

urlpatterns = AUTHENTICATIONS_URLS + USER_URLS