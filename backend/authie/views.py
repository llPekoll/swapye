import logging
import random
import string

import requests
from django.contrib.auth.hashers import check_password, make_password
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.settings import DASHBOARD_DNS, WORKER_DNS

from .models import (
    FeaturesPermission,
    GameDefaults,
    MailingInfo,
    Reset,
    UserAccount,
    UserPersonalInfo,
)
from .serializer import (
    LoginSerializer,
    MailingInfoSerializer,
    TokenSerializer,
    UserPersonalSerializer,
    UserSerializer,
)

logger = logging.getLogger("app")


class FetchUser(APIView):
    def get(self, request, user_uuid):
        user = get_object_or_404(UserAccount, uuid=user_uuid)
        return JsonResponse({"email": user.email})


class FetchUserPermission(APIView):
    def get(self, request):

        user = get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        features = []
        if user.customer_type == "Premium":
            features = FeaturesPermission.objects.using("trad").filter(premium=True)
        elif user.customer_type == "Plus":
            features = FeaturesPermission.objects.using("trad").filter(plus=True)
        elif user.customer_type == "Basic":
            features = FeaturesPermission.objects.using("trad").filter(basic=True)
        elif user.customer_type == "Trial":
            features = FeaturesPermission.objects.using("trad").filter(trial=True)

        features = [feature.name for feature in features]
        return JsonResponse(features, safe=False)


class RegisterAPIView(APIView):
    def post(self, request):
        request.data["email"] = request.data.get("email").lower()
        user_serializer = UserSerializer(data=request.data)
        if not user_serializer.is_valid():
            return JsonResponse({"message": user_serializer.errors}, status=422)
        try:
            user = UserAccount.objects.get(email=request.data.get("email"))
            return JsonResponse({"error": "duplicate"}, status=422)
        except UserAccount.DoesNotExist:
            logger.info("we can create the user")
        user = user_serializer.save()
        user.password = make_password(request.data.get("password"))
        user.save()
        return Response({"message": "user added successfully"})


class LoginAPIView(APIView):
    def post(self, request):
        user_serializer = LoginSerializer(data=request.data)
        if not user_serializer.is_valid():
            return Response({"message": user_serializer.errors}, status=422)
        email = request.data.get("email").lower()
        user = get_object_or_404(UserAccount, email=email)
        if not check_password(request.data.get("password"), user.password):
            return JsonResponse(
                {"error": {"message": "Password is not correct"}}, status=403
            )
        return JsonResponse({"uuid": user.uuid}, status=200)


class EmailCheckAPIView(APIView):
    def post(self, request):
        if not request.data.get("email"):
            return JsonResponse({"error": {"message": "email is missing"}}, status=422)
        try:
            UserAccount.objects.get(email=request.data.get("email"))
        except UserAccount.DoesNotExist:
            return JsonResponse({"success": True})
        return JsonResponse(
            {"error": {"message": "email already in base, please chose another one!"}},
            status=409,
        )


class ForgotAPIView(APIView):
    def post(self, request):
        if not request.data.get("email"):
            return JsonResponse({"error": {"message": "email is missing"}}, status=422)
        token = "".join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(10)
        )
        get_object_or_404(UserAccount, email=request.data.get("email"))
        Reset.objects.create(email=request.data.get("email"), token=token)

        link = f"{DASHBOARD_DNS}/reset/{token}"
        url = f"{WORKER_DNS}/forgot"
        payload = {
            "email": request.data.get("email"),
            "username": request.data.get("email"),
            "link": link,
        }
        requests.post(url, data=payload)
        return JsonResponse({"message": "Un email à été envoyé"})


class ResetAPIView(APIView):
    def post(self, request):
        data = request.data
        token_serializer = TokenSerializer(data=data)
        if not token_serializer.is_valid():
            return Response({"message": token_serializer.errors})
        reset_password = get_object_or_404(Reset, token=data.get("token"))
        user = get_object_or_404(UserAccount, email__iexact=reset_password.email)
        user.password = make_password(data.get("password"))
        user.save()
        Reset.objects.get(token=data.get("token")).delete()
        return JsonResponse({"success": True})


class PersonalsAPIview(APIView):
    def get(self, request):
        user = get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        try:
            return JsonResponse(model_to_dict(user.userpersonalinfo), status=202)
        except UserAccount.userpersonalinfo.RelatedObjectDoesNotExist:
            return JsonResponse(
                {
                    "name": "",
                    "address": "",
                    "postal": "",
                    "phone": "",
                    "siret": "",
                    "rib": "",
                    "company_name": "",
                    "conact_email": "",
                    "city": "",
                }
            )

    def put(self, request):
        user = UserAccount.objects.get(uuid=request.COOKIES.get("session"))
        userpersonal_serializer = UserPersonalSerializer(data=request.data)
        logger.info(userpersonal_serializer)
        if not userpersonal_serializer.is_valid():
            return JsonResponse({"message": userpersonal_serializer.errors}, 422)
        logger.info(userpersonal_serializer.data)
        UserPersonalInfo.objects.update_or_create(
            owner=user, defaults=userpersonal_serializer.data
        )
        up = UserPersonalInfo.objects.get(owner=user)
        return JsonResponse(model_to_dict(up), status=202)


class ApiKeyAPIview(APIView):
    def get(self, request):
        user = UserAccount.objects.get(uuid=request.COOKIES.get("session"))
        try:
            model = model_to_dict(user.mailinginfo)
        except UserAccount.mailinginfo.RelatedObjectDoesNotExist:
            model = {
                "provider": "",
                "apikey": "",
                "apipass": "",
                "email": "",
                "display_name": "",
            }
        model["providers"] = [v for v in MailingInfo.EmailProvider]
        return JsonResponse(model)

    def put(self, request):
        user = UserAccount.objects.get(uuid=request.COOKIES.get("session"))
        mailinginfo_serializer = MailingInfoSerializer(data=request.data)
        if not mailinginfo_serializer.is_valid():
            return Response({"message": mailinginfo_serializer.errors})
        MailingInfo.objects.update_or_create(
            owner=user, defaults=mailinginfo_serializer.data
        )
        mi = MailingInfo.objects.get(owner=user)
        return JsonResponse(model_to_dict(mi), status=202)


class GameDefaultsAPIview(APIView):
    def get(self, request):
        user = UserAccount.objects.get(uuid=request.COOKIES.get("session"))
        try:
            model = model_to_dict(user.gamedefaults)
            if not user.gamedefaults.regulation:
                model["regulation"] = "GET les TRADS"
            if not user.gamedefaults.policy_rules:
                model["policy_rules"] = "GET les TRADS"
            return JsonResponse(model_to_dict(user.gamedefaults))
        except UserAccount.gamedefaults.RelatedObjectDoesNotExist:
            return JsonResponse({"email_check": ""})

    def put(self, request):
        user = UserAccount.objects.get(uuid=request.COOKIES.get("session"))
        data = request.data
        email_check = bool(data.get("email_check"))

        logo = data.get("logo") if data.get("logo") else user.gamedefaults.logo
        music = data.get("music") if data.get("music") else user.gamedefaults.music

        GameDefaults.objects.update_or_create(
            owner=user,
            defaults={
                "email_check": email_check,
                "logo": logo,
                "music": music,
            },
        )
        gd = GameDefaults.objects.get(owner=user)
        return JsonResponse(model_to_dict(gd), status=202)


class RGPDAPIview(APIView):
    def put(self, request):
        user = UserAccount.objects.get(uuid=request.COOKIES.get("session"))
        data = request.data

        regulation = (
            data.get("regulation")
            if data.get("regulation")
            else user.gamedefaults.regulation
        )
        policy_rules = (
            data.get("policy_rules")
            if data.get("policy_rules")
            else user.gamedefaults.policy_rules
        )
        GameDefaults.objects.update_or_create(
            owner=user,
            defaults={"regulation": regulation, "policy_rules": policy_rules},
        )
        return JsonResponse({"success": True})
