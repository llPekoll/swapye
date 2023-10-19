import json
import logging
import re
import tempfile
from datetime import datetime, timedelta

from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from pyexcelerate import Workbook
from rest_framework.views import APIView

from authie.models import FeaturesPermission, GameDefaults, UserAccount
from backend import settings
from games.models import (
    ExtraGameLanguage,
    Game,
    GameTrads,
    Lead,
    Price,
    PricesTrads,
    RequestedElement,
    RequestedElementLead,
    RequestedElementTrads,
    WinnableTimeRange,
    WinnedPrice,
)

from .models import GameType, Skin
from .tools import generate_qr, get_emblem

logger = logging.getLogger("app")


class GameListAPIview(APIView):
    def get(self, request):
        logger.info("Get list of games from user")
        user = get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        games2 = Game.objects.filter(is_active=True, owner=user).values(
            "id",
            "name",
            "emblem",
            "qr_location",
            "game_type__name",
            "game_type__ref_id",
            "skin__ref_id",
            "link",
        )
        games_list = []
        for game in games2:
            if not ExtraGameLanguage.objects.filter(game=game.get("id")):
                gg = Game.objects.get(pk=game.get("id"))
                ExtraGameLanguage.objects.create(
                    game=gg, lang=ExtraGameLanguage.Langues.FR
                )
            games_list.append(
                {
                    "emblem": game.get("emblem"),
                    "name": game.get("name"),
                    "qr_location": game.get("qr_location"),
                    "type": game.get("game_type__name"),
                    "type_id": game.get("game_type__ref_id"),
                    "skin_id": game.get("skin__ref_id"),
                    "link": game.get("link"),
                }
            )
        return JsonResponse({"games": games_list})

    def post(self, request):
        user = get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        body = request.data
        emblem = get_emblem()
        game_link = f"{settings.GAME_DNS}/play/{emblem}"
        game_type, _ = GameType.objects.get_or_create(ref_id=body.get("type"))
        skin, _ = Skin.objects.get_or_create(ref_id=body.get("skin"), game=game_type)
        GameDefaults.objects.get_or_create(owner=user)
        game = Game.objects.create(
            owner=user,
            emblem=emblem,
            link=game_link,
            logo_company=user.gamedefaults.logo,
            qr_location=generate_qr(game_link),
            name=body.get("name"),
            game_type=game_type,
            skin=skin,
            email_check_override=user.gamedefaults.email_check,
        )
        ExtraGameLanguage.objects.create(game=game, lang=ExtraGameLanguage.Langues.FR)
        return JsonResponse({"game_id": game.id, "emblem": game.emblem}, status=201)


class GameDetailAPIview(APIView):
    def get(self, request, emblem):
        owner = get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = Game.objects.filter(Q(emblem=emblem, owner=owner)).first()
        admins = [owner.email, "yoyo.mepa@gmail.com", "benguiguipaul@gmail.com"]
        if not game:
            return JsonResponse({"error": "Game not found"}, status=404)
        if game.owner.email not in admins:
            return JsonResponse({"error": "Game not found"}, status=404)

        model = model_to_dict(game)
        # prices = Price.objects.filter(game=game)
        # w = WinnedPrice.objects.filter(price__in=prices).values_list(
        #     "price__id", flat=True
        # )
        # model["prices"] = []
        # for price in prices:
        #     mod = {
        #         "id": price.id,
        #         "number": price.number,
        #         "name": price.name,
        #         "price_left": list(w).count(price.id),
        #     }
        #     model["prices"].append(mod)

        # model["game_type"] = game.game_type.name
        # model["skin"] = game.skin.name
        model["time_zones"] = [v for v in Game.TimeZone]

        return JsonResponse(model)

    def delete(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        Game.objects.filter(emblem=emblem).update(is_active=False)
        return JsonResponse({"success": True}, status=204)


class GameTypesAndSkinAPIView(APIView):
    def get(self, request):
        user = get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))

        gametypes = []
        gts = GameType.objects.filter(is_active=True)
        for gt in gts.all():
            if len(gt.limited_users.all()) > 0:
                if user in gt.limited_users.all():
                    gametypes.append(model_to_dict(gt))
            else:
                gametypes.append(model_to_dict(gt))
        skins = []
        skns = Skin.objects.filter(is_active=True)
        for skin in skns.all():
            if len(skin.limited_users.all()) > 0:
                if user in skin.limited_users.all():
                    skins.append(model_to_dict(skin))
            else:
                skins.append(model_to_dict(skin))
        for skin in skins:
            del skin["limited_users"]

        for gametype in gametypes:
            del gametype["limited_users"]

        return JsonResponse({"skins": skins, "types": gametypes})


class TimeFrameAPIview(APIView):
    def get(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = get_object_or_404(Game, emblem=emblem)
        start = game.start_date.date()
        end = game.end_date.date()
        dates = [start + timedelta(days=x) for x in range((end - start).days)]
        dates = [x.strftime("%a,%d.%b") for x in dates]

        return JsonResponse({"days": dates})


class DryRunAPIview(APIView):
    def get(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = get_object_or_404(Game, emblem=emblem)
        model = {
            "forceResultWon": game.force_result_won,
            "forceResultLost": game.force_result_lost,
            "forceResultCantReplay": game.force_result_cant_replay,
            "forceResultCantReplayToday": game.force_result_cant_replay_today,
            "dryRun": game.dry_run,
        }
        return JsonResponse(model)

    def put(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        get_object_or_404(Game, emblem=emblem)
        body = request.data
        Game.objects.filter(emblem=emblem).update(
            force_result_won=bool(body.get("forceResultWon")),
            force_result_lost=bool(body.get("forceResultLost")),
            force_result_cant_replay=bool(body.get("forceResultCantReplay")),
            force_result_cant_replay_today=bool(body.get("forceResultCantReplayToday")),
            dry_run=bool(body.get("dryRun")),
        )
        game = Game.objects.get(emblem=emblem)
        return JsonResponse(
            {
                "forceResultWon": game.force_result_won,
                "forceResultLost": game.force_result_lost,
                "forceResultCantReplay": game.force_result_cant_replay,
                "forceResultCantReplayToday": game.force_result_cant_replay_today,
                "dryRun": game.dry_run,
            }
        )


def feature_permission_get(user):
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
    return features


def can_access_feature(user, feature):
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
    if feature in features:
        return True
    return False


class BasicsDetailAPIview(APIView):
    def get(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = get_object_or_404(Game, emblem=emblem)
        return JsonResponse(
            {
                "name": game.name,
                "type": game.game_type.ref_id,
                "skin": game.skin.ref_id,
                "bgIngame": game.bg_ingame,
            }
        )

    def put(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = get_object_or_404(Game, emblem=emblem)
        body = request.data
        print(body)
        game_type = get_object_or_404(GameType, ref_id=body.get("gameType"))
        skin = get_object_or_404(Skin, ref_id=body.get("skin"), game=game_type)
        if body.get("bgUrl"):
            game.bg_ingame = body.get("bgUrl")
        game.name = body.get("name")
        game.game_type = game_type
        game.skin = skin
        game.save()
        return JsonResponse(
            {
                "name": game.name,
                "type": game.game_type.ref_id,
                "skin": game.skin.ref_id,
                "bgIngame": game.bg_ingame,
            }
        )


class FormsAPIView(APIView):
    def get(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = get_object_or_404(Game, emblem=emblem)
        return JsonResponse(
            {
                "formPortrait": game.form_portrait,
                "formLandscape": game.form_landscape,
            }
        )

    def put(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = get_object_or_404(Game, emblem=emblem)
        body = request.data

        if body.get("IntroFormLandscape"):
            game.form_landscape = body.get("IntroFormLandscape")
            game.save()

        if body.get("IntroFormPortrait"):
            game.form_portrait = body.get("IntroFormPortrait")
            game.save()
        return JsonResponse(
            {
                "formPortrait": game.form_portrait,
                "formLandscape": game.form_landscape,
            }
        )


class DateAPIView(APIView):
    def get(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = get_object_or_404(Game, emblem=emblem)

        return JsonResponse(
            {
                "startDate": game.start_date,
                "endDate": game.end_date,
                "startHour": game.starting_time,
                "endHour": game.ending_time,
                "unlimitedInTime": game.unlimited_in_time,
                "losingFactor": game.losing_factor,
                "timeZone": game.timezone,
                "extraLangs": [
                    model_to_dict(lang)
                    for lang in game.extra_langagues.filter(is_active=True)
                ],
            }
        )

    def put(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        body = request.data
        game = get_object_or_404(Game, emblem=emblem)
        game.timezone = body.get("timeZone")
        game.unlimited_in_time = bool(body.get("unlimitedInTime"))

        for lang in json.loads(body.get("extraLangs")):
            ExtraGameLanguage.objects.update_or_create(
                lang=lang, game=game, defaults={"is_active": True}
            )
        for v in ExtraGameLanguage.Langues:
            if v not in json.loads(body.get("extraLangs")):
                logger.info(f">>>>>>>>> HIDE >> {v=}")
                lang = ExtraGameLanguage.objects.filter(
                    lang=v,
                    game=game,
                ).update(is_active=False)

        if body.get("unlimitedInTime"):
            game.losing_factor = body.get("losingFactor")
        else:
            if body.get("startDate"):
                game.start_date = (
                    body.get("startDate") if body.get("startDate") else datetime.now()
                )
            if body.get("endDate"):
                game.end_date = (
                    body.get("endDate") if body.get("endDate") else datetime.now()
                )
            if body.get("startHour"):
                game.starting_time = (
                    body.get("startHour") if body.get("startHour") else datetime.now()
                )
            if body.get("endHour"):
                game.ending_time = (
                    body.get("endHour") if body.get("endHour") else datetime.now()
                )
        game.save()
        return JsonResponse(
            {
                "startDate": game.start_date,
                "endDate": game.end_date,
                "startHour": game.starting_time,
                "endHour": game.ending_time,
                "unlimitedInTime": game.unlimited_in_time,
                "losingFactor": game.losing_factor,
                "timeZone": game.timezone,
                "extraLangs": [
                    model_to_dict(lang)
                    for lang in game.extra_langagues.filter(is_active=True)
                ],
            }
        )


class RequestedAPIView(APIView):
    def get_req(self, game):
        return {
            "requestName": game.request_name,
            "requestTel": game.request_tel,
            "requestAddress": game.request_address,
            "isAlwaysWinner": game.is_always_winner,
            "canReplay": game.can_replay,
            "canReplayToday": game.can_replay_today,
            "emailCheckOverride": game.email_check_override,
        }

    def get(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = get_object_or_404(Game, emblem=emblem)
        model = self.get_req(game)
        return JsonResponse(model)

    def put(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        body = request.data
        Game.objects.filter(emblem=emblem).update(
            request_name=bool(body.get("requestName")),
            request_tel=bool(body.get("requestTel")),
            request_address=bool(body.get("requestAddress")),
            is_always_winner=bool(body.get("isAlwaysWinner")),
            can_replay=bool(body.get("canReplay")),
            can_replay_today=bool(body.get("canReplayToday")),
            email_check_override=bool(body.get("emailCheck")),
        )
        game = Game.objects.get(emblem=emblem)
        model = self.get_req(game)
        return JsonResponse(model)


class ExtraRequestedListAPIView(APIView):
    def get_req(self, game):
        reqs = RequestedElement.objects.filter(game=game, is_active=True)
        extras = []
        for req in reqs:
            langs = []
            for lang in req.requested_elements_lang.all():
                langs.append(
                    {"lang": lang.extra_game_language.lang, "wording": lang.wording}
                )
            extras.append(
                {
                    "id": req.id,
                    "key": req.key,
                    "kind": req.kind,
                    "wordings": langs,
                }
            )
        print(extras)

        langs = [
            model_to_dict(lang) for lang in game.extra_langagues.filter(is_active=True)
        ]
        return {"extraElements": extras, "langs": langs}

    def get(self, request, emblem):
        logger.info(">>>>>>>>> GET EXTRA REQUESTED")
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = get_object_or_404(Game, emblem=emblem)
        reqs = RequestedElement.objects.filter(game=game, is_active=True)
        extras = []
        for req in reqs:
            langs = []
            for lang in req.requested_elements_lang.all():
                langs.append(
                    {"lang": lang.extra_game_language.lang, "wording": lang.wording}
                )
            extras.append(
                {
                    "id": req.id,
                    "key": req.key,
                    "kind": req.kind,
                    "wordings": langs,
                }
            )
        print(extras)

        langs = [
            model_to_dict(lang) for lang in game.extra_langagues.filter(is_active=True)
        ]
        payload = self.get_req(game)
        return JsonResponse(payload)

    def put(self, request, emblem):
        logger.info(">>>>>>>>> PUT EXTRA REQUESTED")
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = get_object_or_404(Game, emblem=emblem)
        body = request.data
        filtered_reqelt = []
        for extraElt in body.get("extraElts"):
            newdir = {}
            for elt in extraElt:
                if "option" in elt.get("key"):
                    newdir["kind"] = elt["val"]
                if "id" in elt.get("key").split(","):
                    newdir["id"] = int(elt["val"])
                if "key" in elt.get("key") and len(elt.get("key")) < 15:
                    newdir["key"] = elt["val"]
            newdir["langs"] = {
                elt.get("key").split(",")[2][3:]: elt.get("val")
                for elt in extraElt
                if len(elt.get("key")) > 10 and "id" not in elt.get("key")
            }

            filtered_reqelt.append(newdir)
        for elt in filtered_reqelt:
            if elt.get("id") == 0:
                print(">>>>>>>>> CREATE")
                req = RequestedElement.objects.create(
                    game=game,
                    kind=elt.get("kind").capitalize(),
                    key=elt.get("key"),
                )
                RequestedElementTrads.objects.filter(requested_element=req).delete()
                for lang in elt.get("langs"):
                    RequestedElementTrads.objects.create(
                        requested_element=req,
                        extra_game_language=ExtraGameLanguage.objects.get(
                            lang__contains=lang, game=game
                        ),
                        wording=elt.get("langs")[lang],
                    )
            else:
                print(">>>>>>>>> EDIT")
                if elt.get("id"):
                    req = RequestedElement.objects.get(id=elt.get("id"))
                    req.kind = elt.get("kind").capitalize()
                    req.save()
                    RequestedElementTrads.objects.filter(requested_element=req).delete()
                    for lang in elt.get("langs"):
                        if elt.get("langs").get(lang) != {}:
                            RequestedElementTrads.objects.create(
                                requested_element=req,
                                extra_game_language=ExtraGameLanguage.objects.get(
                                    lang__contains=lang, game=game
                                ),
                                wording=elt.get("langs")[lang],
                            )
        game.refresh_from_db()
        payload = self.get_req(game)
        return JsonResponse(payload)


class ExtraRequestedDetailAPIView(APIView):
    def delete(self, request, emblem, id):
        print(f">>>>>>>>> DELETE >>{id=}")
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = get_object_or_404(Game, emblem=emblem)
        req = RequestedElement.objects.get(game=game, id=id)
        RequestedElement.objects.filter(game=game, key=req.key).update(is_active=False)
        print(">>>>>>>>> hidden >>")
        return JsonResponse({"success": True})


class SalonModeAPIView(APIView):
    def get_salon(self, game):
        return {
            "fullScreenBtn": game.fullscreen_btn,
            "restartBtn": game.restart_btn,
            "automaticRestart": game.automatic_restart_activated,
            "automaticRestartCounterValue": game.automatic_restart_counter_value,
            "soundOveride": game.sound_overide,
        }

    def get(self, request, emblem):
        user = get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = Game.objects.get(emblem=emblem)
        GameDefaults.objects.get_or_create(owner=user)
        model = self.get_salon(game)
        return JsonResponse(model)

    def put(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = get_object_or_404(Game, emblem=emblem)
        body = request.data
        print(body)
        game.fullscreen_btn = bool(body.get("fullscreen_btn"))
        game.restart_btn = bool(body.get("restart_btn"))
        game.automatic_restart_activated = bool(body.get("automatic_restart"))
        game.automatic_restart_counter_value = (
            body.get("timer") if body.get("timer") else 20
        )
        if isinstance(body.get("music"), str) and "https" in body.get("music"):
            game.sound_overide = body.get("music")
        game.save()

        game.refresh_from_db()
        payload = self.get_salon(game)
        return JsonResponse(payload)


class SocialMediaAPIView(APIView):
    def get(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = Game.objects.get(emblem=emblem)
        model = {
            "facebook": game.facebook,
            "insta": game.insta,
            "twitter": game.twitter,
        }
        return JsonResponse(model)

    def put(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        body = request.data
        Game.objects.filter(emblem=emblem).update(
            facebook=body.get("facebook"),
            insta=body.get("insta"),
            twitter=body.get("twitter"),
        )
        return JsonResponse({"success": True})


class GameIdentityAPIView(APIView):
    def get_identity(self, game):
        trads_pack = []
        for trads in ExtraGameLanguage.objects.filter(game=game, is_active=True).all():
            logger.info(f"{trads=}")
            if not GameTrads.objects.filter(extra_game_language=trads):
                GameTrads.objects.create(extra_game_language=trads)
            game_trads = GameTrads.objects.get(extra_game_language=trads)
            logger.info(f"{game_trads=}")
            pack = {
                "lang": trads.lang,
                "openingText": game_trads.opening_text,
                "closingText": game_trads.closing_text,
            }
            trads_pack.append(pack)
        return {
            "logoCompany": game.logo_company,
            "openingText": game.opening_text,
            "closingText": game.closing_text,
            "langs": trads_pack,
            "color": game.color,
        }

    def get(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = get_object_or_404(Game, emblem=emblem)
        payload = self.get_identity(game)
        return JsonResponse(payload)

    def put(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        body = request.data
        game = get_object_or_404(Game, emblem=emblem)

        if body.get("opening_texts"):
            for k, v in body.get("opening_texts").items():
                k = k.replace("opening_text_", "")
                el = ExtraGameLanguage.objects.get(lang__contains=k[9:], game=game)
                if el:
                    opening = GameTrads.objects.get(extra_game_language=el)
                    opening.opening_text = v
                    opening.save()
                else:
                    GameTrads.objects.create(extra_game_language=el, opening_text=v)

        if body.get("closing_texts"):
            for k, v in body.get("closing_texts").items():
                k = k.replace("closing_text_", "")
                el = ExtraGameLanguage.objects.get(lang__contains=k[9:], game=game)
                if el:
                    closing = GameTrads.objects.get(extra_game_language=el)
                    closing.closing_text = v
                    closing.save()
                else:
                    GameTrads.objects.create(extra_game_language=el, closing_text=v)

        el = ExtraGameLanguage.objects.filter(game=game).first()
        opening = (
            el.game_traductions.first().opening_text if el else body.get("opening_text")
        )
        closing = (
            el.game_traductions.first().closing_text if el else body.get("closing_text")
        )
        if body.get("logo_company"):
            game.logo_company = body.get("logo_company")
        if body.get("color"):
            game.color = body.get("color")
        game.opening_text = opening
        game.closing_text = closing
        game.save()
        game.refresh_from_db()
        payload = self.get_identity(game)
        return JsonResponse(payload)


class PriceDetailAPIview(APIView):
    def get(self, request, emblem, id):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = Game.objects.get(emblem=emblem)
        price = get_object_or_404(Price, game=game, id=id)
        langs = ExtraGameLanguage.objects.filter(game=game, is_active=True).all()
        langs = [model_to_dict(lang) for lang in langs]

        model = model_to_dict(price)
        print(model)
        trad_prices = []
        for trads in ExtraGameLanguage.objects.filter(game=game, is_active=True).all():
            if trads.price_traductions == price:
                trad_prices.append(trads.price_traductions)
        model["id"] = price.id
        trads = PricesTrads.objects.filter(price=price)

        langs = []
        trad_pack = []
        for trad in trads:
            traduction = {
                "lang": trad.extra_game_language.lang,
                "src": trad.img,
                "name": trad.name,
            }
            trad_pack.append(traduction)
            langs.append(model_to_dict(trad.extra_game_language))

        model["lang"] = langs
        model["trads"] = trad_pack
        timetable = WinnableTimeRange.objects.filter(price=price)
        timetable = [t.number for t in timetable]

        langs = ExtraGameLanguage.objects.filter(game=game, is_active=True).all()
        langs = [model_to_dict(lang) for lang in langs]
        return JsonResponse({"price": model, "timetable": timetable, "langs": langs})

    def put(self, request, emblem, id):

        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        body = request.data
        game = Game.objects.get(emblem=emblem)
        price = get_object_or_404(Price, id=id, game=game)
        logger.info("found price")
        WinnableTimeRange.objects.filter(price=price).delete()
        if game.start_date:
            start = game.start_date.date()
            end = game.end_date.date()
            dates = [start + timedelta(days=x) for x in range((end - start).days)]

            if body.get("winnableTimeRage"):
                i = 0
                for values in body.get("winnableTimeRage"):
                    if values == "":
                        values = 0
                    WinnableTimeRange.objects.create(
                        price=price, day=dates[i], number=values
                    )
                    i += 1

        name = ""

        if body.get("trads"):
            for k, v in body.get("trads").items():
                if "name" in v:
                    name = v.get("name").replace("trads", game.name)
                if name:
                    break
        else:
            name = body.get("name")
        if body.get("trads"):
            for k, v in body.get("trads").items():
                el = ExtraGameLanguage.objects.get(lang__contains=k, game=game)
                if v.get("img"):
                    PricesTrads.objects.filter(
                        price=price, extra_game_language=el
                    ).update(img=v.get("img"))
                if v.get("name"):
                    price.name = (
                        f'{v.get("name")}' if f'trads-{v.get("name")}' else "trads-"
                    )
                    price.save()
                    PricesTrads.objects.filter(
                        price=price, extra_game_language=el
                    ).update(name=v.get("name"))
        if body.get("img"):
            price.img = body.get("img")
        price.number = body.get("quantity")
        price.display_price_name = bool(body.get("display_price_name"))
        price.offset_price_name = body.get("offset_price_name")
        price.email_template = body.get("email_template")
        price.consolation_price = bool(body.get("consolation_price"))
        price.unlimited_in_time = game.unlimited_in_time
        price.save()
        price.refresh_from_db()
        timetable = WinnableTimeRange.objects.filter(price=price)
        timetable = [t.number for t in timetable]
        payload = {
            "id": price.id,
            "name": price.name,
            "number": price.number,
            "img": price.img,
            "unlimitedInTime": price.unlimited_in_time,
            "email_template": price.email_template,
            "consolation_price": price.consolation_price,
            "display_price_name": price.display_price_name,
            "timetable": timetable,
        }
        return JsonResponse(payload, status=202)

    def delete(self, request, emblem, id):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = Game.objects.get(emblem=emblem)
        try:
            Price.objects.get(id=id, game=game).delete()
        except Price.DoesNotExist:
            return JsonResponse({"error": {"message": "object not found"}})
        return JsonResponse({"success": True}, status=204)


class EnableQrRecpetionAPIview(APIView):
    def post(self, request, emblem):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        body = request.data
        game = Game.objects.get(emblem=emblem)
        game.use_qr_for_games = bool(body.get("enable_qr"))
        game.save()
        return JsonResponse({"enable_qr": game.use_qr_for_games})


class PriceListAPIview(APIView):
    def get(self, request, emblem, type):
        if type == "dash":
            get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        game = get_object_or_404(Game, emblem=emblem)
        prices = Price.objects.filter(game=game)
        price_list = []
        langs = ExtraGameLanguage.objects.filter(game=game, is_active=True).all()
        langs = [model_to_dict(lang) for lang in langs]
        if game.game_type.ref_id == 3 and type == "game":  #  jackpot return
            price_list = []
            for price in prices:
                ret = {"id": "", "type": "", "wordings": [{"lang": "", "value": ""}]}
                ret["id"] = price.id
                if price.price_traductions.first():
                    print(price.price_traductions.first().img)
                    ret["type"] = (
                        "text" if price.price_traductions.first().img == "" else "image"
                    )
                ret["wordings"] = []
                for trad in PricesTrads.objects.filter(price=price).all():
                    ret["wordings"].append(
                        {
                            "lang": trad.extra_game_language.lang,
                            "value": trad.img if not trad.img == "" else trad.name,
                        }
                    )
                price_list.append(ret)
                print(price_list)
            return JsonResponse(price_list, safe=False)

        for price in prices:
            model = model_to_dict(price)
            trad_prices = []
            for trads in ExtraGameLanguage.objects.filter(
                game=game, is_active=True
            ).all():
                if trads.price_traductions == price:
                    trad_prices.append(trads.price_traductions)
            model["id"] = price.id
            model["name"] = price.name
            model["img"] = price.img
            trads = PricesTrads.objects.filter(price=price)
            trad_pack = []
            for trad in trads:
                traduction = {
                    "lang": trad.extra_game_language.lang,
                    "src": trad.img,
                    "name": trad.name,
                }
                trad_pack.append(traduction)
            model["lang"] = langs
            model["trads"] = trad_pack
            model["trads"] = trad_pack
            price_list.append(model)
            timetable = WinnableTimeRange.objects.filter(price=price)
            model["timetable"] = [t.number for t in timetable]

            model["price_won"] = WinnedPrice.objects.filter(price=price.id).count()

        langs = ExtraGameLanguage.objects.filter(game=game, is_active=True)
        langs = [model_to_dict(lang) for lang in langs]
        price_list = [
            {
                "id": price["id"],
                "name": price["name"],
                "img": price["img"],
                "number": price["number"],
                "offsetPriceName": price["offset_price_name"],
                "displayPriceName": price["display_price_name"],
                "emailTemplate": price["email_template"],
                "consolationPrice": price["consolation_price"],
            }
            for price in price_list
        ]
        logger.info(f"Prices List \n {price_list}")

        return JsonResponse(
            {
                "prices": price_list,
                "langs": langs,
                "enable_qr": game.use_qr_for_games,
            }
        )

    def post(self, request, emblem, type):
        get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        body = request.data
        game = Game.objects.get(emblem=emblem)
        name = ""
        if body.get("trads"):
            for k, v in body.get("trads").items():
                if "name" in v:
                    name = v.get("name")
                if name:
                    break
        price = Price.objects.create(
            game=game,
            name=name,
            number=body.get("quantity"),
            display_price_name=bool(body.get("display_price_name")),
            offset_price_name=body.get("offset_price_name")
            if body.get("offset_price_name")
            else "",
            email_template=body.get("email_template"),
            consolation_price=bool(body.get("consolation_price")),
        )
        WinnableTimeRange.objects.filter(price=price).delete()
        img = ""
        if body.get("trads"):
            logger.info("trads")
            logger.info(body.get("trads"))
            for k, v in body.get("trads").items():
                el = ExtraGameLanguage.objects.get(lang__contains=k, game=game)
                PricesTrads.objects.create(
                    price=price,
                    extra_game_language=el,
                    name=v.get("name") if v.get("name") else "",
                    img=v.get("img") if v.get("img") else "",
                )
                if v.get("img"):
                    img = v.get("img")
            price.img = img
            price.save()
        else:
            el = ExtraGameLanguage.objects.filter(game=game).first()
            PricesTrads.objects.create(
                price=price,
                extra_game_language=el,
                name=body.get("name") if body.get("name") else "",
                img=body.get("img") if body.get("img") else "",
            )

        if game.start_date:
            start = game.start_date.date()
            end = game.end_date.date()
            dates = [start + timedelta(days=x) for x in range((end - start).days)]
            if body.get("winnableTimeRage"):
                i = 0
                for values in body.get("winnableTimeRage"):
                    if values == "":
                        values = 0
                    WinnableTimeRange.objects.create(
                        price=price, day=dates[i], number=values
                    )
                    i += 1
        return JsonResponse({"id": price.id}, status=201)


def generate_all_xlsx(id):
    user = UserAccount.objects.get(uuid=id)
    games = Game.objects.filter(owner=user)
    wb = Workbook()

    for i, game in enumerate(games):
        leads = Lead.objects.filter(game=game)
        reqs = RequestedElementLead.objects.filter(lead__in=leads)
        extra = [json.dumps({req.requested_element.key: req.value}) for req in reqs]
        prices_name = [
            lead.price_won.price.name if lead.price_won else "Perdu" for lead in leads
        ]
        headers = [
            "Number",
            "date",
            "email",
            "name",
            "phone",
            "address",
            "can reveceive email",
            "price won",
            "Requested elements",
        ]

        rows = []
        rows.append(headers)
        for i, lead in enumerate(leads):
            row = [
                i,
                lead.creation_date.strftime("%A, %d. %B %Y %I:%M%p"),
                lead.email,
                lead.name,
                lead.phone,
                lead.address,
                lead.can_reveceive_email,
                prices_name[i],
                extra[i] if len(extra) >= i + 1 else "",
            ]
            rows.append(row)
        game_name = re.sub("\W+", "_", game.name[:31])
        wb.new_sheet(f"i_{game_name}", data=rows)
    output = tempfile.NamedTemporaryFile(delete=True, suffix=".xlsx")
    wb.save(output.name)

    return output


def generate_single_xlsx(game):

    leads = Lead.objects.filter(game=game)
    reqs = RequestedElementLead.objects.filter(lead__in=leads)
    extra = [json.dumps({req.requested_element.key: req.value}) for req in reqs]
    prices_name = [
        lead.price_won.price.name if lead.price_won else "Perdu" for lead in leads
    ]
    headers = [
        "Number",
        "date",
        "email",
        "name",
        "phone",
        "address",
        "can reveceive email",
        "price won",
        "Requested elements",
    ]

    rows = []
    rows.append(headers)
    for i, lead in enumerate(leads):
        row = [
            i,
            lead.creation_date.strftime("%A, %d. %B %Y %I:%M%p"),
            lead.email,
            lead.name,
            lead.phone,
            lead.address,
            lead.can_reveceive_email,
            prices_name[i],
            extra[i] if len(extra) >= i + 1 else "",
        ]
        rows.append(row)
    wb = Workbook()
    game_name = re.sub("\W+", "_", game.name[:31])

    wb.new_sheet(game_name, data=rows)
    output = tempfile.NamedTemporaryFile(delete=True, suffix=".xlsx")
    wb.save(output.name)
    return output


class ExcellAPIView(APIView):
    def get(self, request, id):

        output = generate_all_xlsx(id)
        filename = "export_swapye.xlsx"
        response = HttpResponse(
            output,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response


class ExcellSingleAPIView(APIView):
    def get(self, request, id, emblem):
        get_object_or_404(UserAccount, uuid=id)
        game = get_object_or_404(Game, emblem=emblem)
        output = generate_single_xlsx(game)
        filename = "export_swapye.xlsx"
        response = HttpResponse(
            output,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response


class CheckValidEmails(APIView):
    def get(self, request, emblem):
        game = get_object_or_404(Game, emblem=emblem)
        leads = Lead.objects.filter(game=game)
        valid = []
        unvalid = []
        for lead in leads:
            if re.match(
                r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", lead.email
            ):
                valid.append(lead.email)
            else:
                unvalid.append(lead.email)
        return JsonResponse(
            {
                "valid": valid,
                "valid_nb": len(valid),
                "unvalid": unvalid,
                "unvalid_nb": len(unvalid),
            }
        )
