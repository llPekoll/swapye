from django.urls import path

from .views import (
    ApiKeyAPIview,
    EmailCheckAPIView,
    FetchUser,
    FetchUserPermission,
    ForgotAPIView,
    LoginAPIView,
    GameDefaultsAPIview,
    PersonalsAPIview,
    RegisterAPIView,
    ResetAPIView,
)

urlpatterns = [
    path("auth/login", LoginAPIView.as_view()),
    path("auth/user/<uuid:user_uuid>", FetchUser.as_view()),
    path("auth/register", RegisterAPIView.as_view()),
    path("auth/rights", FetchUserPermission.as_view()),
    path("auth/forgot", ForgotAPIView.as_view()),
    path("auth/reset", ResetAPIView.as_view()),
    path("auth/email_checker", EmailCheckAPIView.as_view()),
    path("gamedefaults", GameDefaultsAPIview.as_view()),
    path("rgpd", GameDefaultsAPIview.as_view()),
    path("personals", PersonalsAPIview.as_view()),
    path("apikey", ApiKeyAPIview.as_view()),
]
