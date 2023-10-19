import logging
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from games.models import Game
from authie.models import UserAccount, GameDefaults

logger = logging.getLogger("app")


class BgInGameAPIView(APIView):
    def delete(self, request, emblem):
        logger.info(f">>>>>>>>> Delete BG in game")
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        Game.objects.filter(emblem=emblem).update(bg_ingame="")
        return JsonResponse({"success": True})


class FormLandScapeAPIView(APIView):
    def delete(self, request, emblem):
        logger.info(f">>>>>>>>> Delete Form landscape")
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        Game.objects.filter(emblem=emblem).update(form_landscape="")
        return JsonResponse({"success": True})


class FormPortraitAPIView(APIView):
    def delete(self, request, emblem):
        logger.info(f">>>>>>>>> Delete Form portrait")
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        Game.objects.filter(emblem=emblem).update(form_portrait="")
        return JsonResponse({"success": True})


class LogoAPIView(APIView):
    def delete(self, request, emblem):
        logger.info(f">>>>>>>>> Delete Logo")
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        Game.objects.filter(emblem=emblem).update(logo_company="")
        return JsonResponse({"success": True})


class SoundAPIView(APIView):
    def delete(self, request, emblem):
        logger.info(f">>>>>>>>> Delete sound")
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        Game.objects.filter(emblem=emblem).update(sound_overide="")
        return JsonResponse({"success": True})


class LogoDefaultAPIView(APIView):
    def delete(self, request):
        logger.info(f">>>>>>>>> Delete logo default")
        user = get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))

        GameDefaults.objects.filter(owner=user).update(logo="")
        return JsonResponse({"success": True})


class SoundDefaultAPIView(APIView):
    def delete(self, request):
        logger.info(f">>>>>>>>> Delete sound default")
        user = get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        GameDefaults.objects.filter(owner=user).update(music="")
        return JsonResponse({"success": True})
