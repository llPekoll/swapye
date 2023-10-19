import json
import logging
from datetime import date, datetime

import boto3
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.db.models import Count
from django.db.models.functions import TruncMonth

import backend.settings as settings
from authie.models import UserAccount
from games.models import Game, Price, PricesTrads, WinnedPrice, WinnableTimeRange, Lead

logger = logging.getLogger("app")

session = boto3.session.Session()
client = session.client(
    "s3",
    region_name=settings.AWS_S3_REGION_NAME,
    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


class GameValidatorAPIview(APIView):
    def get(self, request, emblem):
        game = get_object_or_404(Game, emblem=emblem)
        errors = []
        warnings = []
        if game.prices.count() == 0:
            logger.error("this game need at least one price")
            errors.append("il vous faut au moins un lot pour ce jeux")
        # Jackpot if not 3 prices
        if game.game_type.ref_id == 3:
            prices = Price.objects.filter(game=game)
            if len(prices) <= 2:
                logger.error("this game need at least 3 prices to run")
                errors.append("il vous faut au moins 3 lots pour ce jeux")
        # check for table prices
        ws = []
        if not game.unlimited_in_time:
            for price in game.prices.all():
                w = WinnableTimeRange.objects.filter(price=price, number__gt=0)
                if w.exists():
                    ws.append(w)
            if len(ws) == 0:
                logger.warning("care no timble for that game")
                warnings.append(
                    "la timetable n'est pas rempli, ce n'est pas grave, mais c'est entre les mains du hazard"
                )

        # ulimited on time or date start date end
        if not game.unlimited_in_time:
            if game.start_date is None or game.end_date is None:
                logger.error("this game need a start date/ end date")
                errors.append("Il vous faut une date de début/ fin pour ce jeux")
        # check for consolation price
        prices = Price.objects.filter(consolation_price=True, game=game)

        if game.is_always_winner and len(prices) == 0:
            logger.warning(
                "====== NOT SAFE =====\nGame Is Unlimited In Time And Not Consolation Prices"
            )
            warnings.append(
                "votre jeux est reglé sur toujours gagants, mais vous n'avez pas de lot de consolation, assurer vous davoir assez de lot."
            )

        # TODO email cehck is activated and
        # prices = Price.objects.filter(consolation_price=True, game=game)

        # if game.is_always_winner and len(prices) == 0:
        #     logger.warning("care game is unlimited in time and not consolation prices")
        #     warnings.append(
        #         "votre jeux est reglé sur toujours gagants, mais vous n'avez pas de lot de consolation, assurer vous davoir assez de lot."
        #     )

        return JsonResponse(
            {"errors": errors, "warnings": warnings},
            status=200,
        )


class BackupAllAPIview(APIView):
    def get(self, request):
        for user in UserAccount.objects.all():
            dest = f"backup/{settings.STATE}/{user.email}/{str(date.today())}.json"
            games = {}
            for game in user.games.all():
                leads = [model_to_dict(lead) for lead in game.leads.all()]
                games[game.name] = leads
            client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=dest,
                Body=json.dumps(games),
                ContentType="application/json",
            )
            logger.info(f"Backup for {user.email} done")
        return JsonResponse({"success": True}, status=200)


class ExportPaulAPIview(APIView):
    def get(self, request):
        obj = {}
        leads = (
            Lead.objects.annotate(month=TruncMonth("creation_date"))
            .values("month", "game__owner__email")
            .annotate(total=Count("id"))
        )
        for lead in leads:
            if lead["month"].strftime("%Y-%m") in obj:
                obj[lead["month"].strftime("%Y-%m")][lead["game__owner__email"]] = lead[
                    "total"
                ]
            else:
                obj[lead["month"].strftime("%Y-%m")] = {
                    lead["game__owner__email"]: lead["total"]
                }
        print(obj)
        return JsonResponse(obj, status=200)


class UnlockPriceAPIview(APIView):
    def get(self, request, tiny):
        w = WinnedPrice.objects.filter(price_code=tiny).first()
        logger.info(f"{w.price_taken=}")
        price_trads = PricesTrads.objects.filter(price=w.price).first()
        logger.info(f"{price_trads=}")
        if w.price_taken:
            return JsonResponse(
                {
                    "message": f"""  Le lot a déjà été pris ❌<br/>
                                    Price already taken ❌ <br/>
                                    {price_trads.name}<br/>
                                    Pickup date: { w.picked_date.strftime("%A, %d. %B %Y %I:%M%p")}<br/>""",
                    "status": "error",
                },
                status=200,
            )

        img = (
            f'<img src="{price_trads.img}" alt="price img"/>' if price_trads.img else ""
        )
        return JsonResponse(
            {
                "message": f""" Lot Disponible ✔<br/>
                            Price available ✔ <br/>
                            {price_trads.name} <br/>
                            {img}""",
                "status": "success",
            },
            status=200,
        )

    def post(self, request, tiny):
        print(f"{tiny=}")
        WinnedPrice.objects.filter(price_code=tiny).update(
            price_taken=True, picked_date=datetime.now()
        )
        return JsonResponse(
            {"success": True},
            status=200,
        )
