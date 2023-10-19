import logging
from datetime import date, datetime, time, timedelta
from random import choice, choices, shuffle, uniform

import pytz
import requests
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.views import APIView

from authie.models import UserAccount
from backend.settings import BOUNCER_API_KEY, DASHBOARD_DNS
from dash.tools import generate_qr_price, get_code_price
from mails.tools import send_email
from trads.models import Trad

from .models import (
    Game,
    Lead,
    Price,
    RefusedLead,
    RequestedElement,
    RequestedElementLead,
    ValidatedEmail,
    WinnableTimeRange,
    WinnedPrice,
)

logger = logging.getLogger("app")


def get_total_number_of_days(game):
    if not game.end_date or not game.start_date:
        return 0
    nb_days = abs(game.end_date - game.start_date)
    return nb_days


class EmailValidationAPIView(APIView):
    def post(self, request):
        logger.info(f"EmailValidationAPIView: {request.data=}")
        email = request.data.get("email")
        if not email:
            return JsonResponse({"error": "no email"}, status=422)

        url = f"https://api.usebouncer.com/v1/email/verify?email={email}&timeout=10"
        headers = {"x-api-key": BOUNCER_API_KEY}
        response = requests.request("GET", url, headers=headers)
        ret = response.json()
        logger.info(f"check mail {ret=}")
        game = get_object_or_404(Game, emblem=request.data.get("emblem"))
        logger.info(f"{game=}")
        if ret["status"] == "deliverable":
            validated_email = ValidatedEmail.objects.create(
                email=email, game=game, bouncer_return=ret, validated=True
            )
            logger.info(f" validation works {validated_email=}")
            return JsonResponse(
                {"status": "valid", "id": validated_email.id}, status=200
            )

        validated_email = ValidatedEmail.objects.create(
            email=email, game=game, bouncer_return=ret, validated=False
        )
        logger.info(f" validation fail {validated_email=}")
        return JsonResponse({"status": "wrong", "id": validated_email.id}, status=200)


class PlayAPIView(APIView):
    def get(self, request, emblem):
        logger.info(f"Game Has Been Lanched => {emblem=}")
        game = get_object_or_404(Game, emblem=emblem, is_active=True)
        model = {
            "emblem": game.emblem,
            "name": game.name,
            "logo": game.logo_company,
            "gameType": game.game_type.name,
            "skin": game.skin.name,
            "gameTypeIdRef": game.game_type.ref_id,
            "skinIdRef": game.skin.ref_id,
            "emailCheck": game.email_check_override,
            "fullscreenBtn": game.fullscreen_btn,
            "formColor": game.color,
            "dryRun": game.dry_run,
            "bgIngame": game.bg_ingame,
            "formPortrait": game.form_portrait,
            "formLandscape": game.form_landscape,
            "restartBtn": game.restart_btn,
            "automaticRestart": game.automatic_restart_activated,
            "automaticRestartCounterValue": game.automatic_restart_counter_value,
            "requestName": game.request_name,
            "requestTel": game.request_tel,
            "requestAddress": game.request_address,
            "unlimitedInTime": game.unlimited_in_time,
            "startDate": game.start_date,
            "endDate": game.end_date,
        }

        if not game.sound_overide:
            if game.owner.gamedefaults:
                model["music"] = game.owner.gamedefaults.music
        else:
            model["music"] = game.sound_overide

        # logger.info(f"model base {model=}")
        # can be done in 1 query
        reqs = RequestedElement.objects.filter(game=game, is_active=True)
        extras = []
        # logger.info(f"{reqs=}")
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
        if game.game_type.ref_id == 2:
            model["winnerDay"] = date.today().day
            tt = get_total_number_of_days(game)
            if tt:
                model["numberOfDays"] = [
                    (game.start_date + timedelta(days=b)).day for b in range(tt.days)
                ]
                shuffle(model["numberOfDays"])
            else:
                model["numberOfDays"] = []
        model["extraRequested"] = extras
        return JsonResponse(model)


def get_time_left(game):
    dt = pytz.timezone("Europe/Paris")
    now = datetime.now(tz=dt)
    tme = now.time()
    clean = time(minute=tme.minute, hour=tme.hour)
    ending_time = game.ending_time if game.ending_time else time(hour=19)
    starting_time = game.starting_time if game.starting_time else time(hour=9)
    FMT = "%H:%M:%S"
    if ending_time <= clean:
        # in case of game 2 for exemple start time and end time is not set
        ending_time = time(minute=59, hour=23)

    tdelta = datetime.strptime(str(ending_time), FMT) - datetime.strptime(
        str(clean), FMT
    )
    hh, mm, ss = map(int, str(tdelta))
    
    return (hh * 60) + mm
    

def is_winning(game):
    """Choose if we have a winner or not
    Args:
        game (Game): Game model

    Returns:
        Boolean: returns True if winner, False if looser
    """
    prices_won = WinnedPrice.objects.filter(game=game).count()
    price_total = 0
    for prices in game.prices.all():
        price_total += prices.number
    left_to_win = price_total - prices_won
    # check if we still have prices
    if left_to_win <= 0:
        logger.info(f"Lost Bcz no more prices")
        return False
    d1 = datetime(
        year=game.end_date.year,
        month=game.end_date.month,
        day=game.end_date.day,
    )
    time_left_for_that_day = get_time_left(game)
    delta = abs((datetime.today() - d1).days)
    if delta == 0:
        delta = 1
    player_minutes = 2
    v = uniform(0, 1)
    if v > player_minutes:
        logger.info(f"Lost Bcz no more prices")
        return False
    logger.info(f"Won")
    return True


def get_price(game):
    in_bank = []
    for price in game.prices.all():
        prices_won = WinnedPrice.objects.filter(
            game=game, price=price, creation_date__date=date.today()
        ).count()
        left_to_win = price.number - prices_won
        w = WinnableTimeRange.objects.filter(price=price, number__gt=0)
        if len(w) > 0:
            logger.info(f"Using time table")
            time_ranges = WinnableTimeRange.objects.filter(
                day=date.today(), number__gt=0, price=price
            )
            for time_range in time_ranges:
                logger.info(
                    f"Price Name: {price.name},{price.id},\n Time Range:{time_range.number},\n Price Already Won: {prices_won}"
                )
                left_to_win = time_range.number - prices_won
                if left_to_win > 0:
                    res = [price.id, left_to_win]
                    in_bank.append(res)
        else:
            logger.info(f"Unlimited in time ")
            if game.unlimited_in_time:
                if left_to_win > 0:
                    res = [price.id, left_to_win]
                    logger.info(f"Prices Left {price.name}, {res=}")
                    in_bank.append(res)
                else:
                    logger.info(
                        f"price Left To Win Is {left_to_win=} \n Price Won {prices_won=}"
                    )
            else:
                d1 = datetime(
                    year=game.end_date.year,
                    month=game.end_date.month,
                    day=game.end_date.day,
                )
                delta = abs((datetime.today() - d1).days)
                if delta == 0:
                    delta = 1
                for_today = left_to_win / delta

                if not for_today <= 0:
                    res = [price.id, for_today]
                    in_bank.append(res)

    vals = [v[0] for v in in_bank]
    factor = [v[1] for v in in_bank]
    if len(in_bank) == 0:
        return "1", factor[0]
    
    return factor[0], price



class LeadDetailAPIView(APIView):
    def get(self, request, emblem):
        game = get_object_or_404(Game, emblem=emblem)
        leads = Lead.objects.filter(game=game).values(
            "email",
            "phone",
            "address",
            "name",
            "price_won__price__name",
            "creation_date",
            "requested_elements__value",
            "requested_elements__requested_element__key",
        )
        ll = []
        for lead in leads:
            reqs = []
            for jose in leads:
                if jose.get("email") == lead.get("email"):
                    if jose.get("requested_elements__requested_element__key"):
                        reqs.append(
                            {
                                jose.get(
                                    "requested_elements__requested_element__key"
                                ): jose.get("requested_elements__value")
                            }
                        )

            res = {
                "email": lead.get("email"),
                "phone": lead.get("phone"),
                "address": lead.get("address"),
                "name": lead.get("name"),
                "price_won": lead.get("price_won__price__name"),
                "creation_date": lead.get("creation_date").strftime(
                    "%A, %d. %B %Y %I:%M%p"
                ),
                "extras": reqs,
            }

            ll.append(res)
        return JsonResponse(ll, safe=False)


class LeadAPIView(APIView):
    def get(self, request):
        logger.info(" ============= get lead ============")
        user = get_object_or_404(UserAccount, uuid=request.COOKIES.get("session"))
        games = Game.objects.filter(owner=user)
        total_leads = Lead.objects.filter(game__in=games).count()
        gg = []
        for game in games:
            leads = Lead.objects.filter(game=game).count()
            leads = Lead.objects.filter(game=game).values(
                "email",
                "phone",
                "address",
                "name",
                "price_won__price__name",
                "creation_date",
                "requested_elements__value",
                "requested_elements__requested_element__key",
            )
            ll = []
            for lead in leads:
                reqs = []
                for jose in leads:
                    if jose.get("email") == lead.get("email"):
                        if jose.get("requested_elements__requested_element__key"):
                            reqs.append(
                                {
                                    jose.get(
                                        "requested_elements__requested_element__key"
                                    ): jose.get("requested_elements__value")
                                }
                            )

                res = {
                    "email": lead.get("email"),
                    "phone": lead.get("phone"),
                    "address": lead.get("address"),
                    "name": lead.get("name"),
                    "price_won": lead.get("price_won__price__name"),
                    "creation_date": lead.get("creation_date").strftime(
                        "%A, %d. %B %Y %I:%M%p"
                    ),
                    "extras": reqs,
                }
                if not res in ll:
                    ll.append(res)
            gg.append(
                {
                    "name": game.name,
                    "emblem": game.emblem,
                    "leads": list(ll),
                }
            )

        return JsonResponse({"signe_leads": gg, "total_leads": total_leads})

    def post(self, request):
        body = request.data
        logger.info(f"====== Game have been Played {body.get('emblem')}======")
        game = get_object_or_404(Game, emblem=body.get("emblem"))

        if game.force_result_lost:
            logger.info("====== force_result_lost ======")
            return JsonResponse(
                {
                    "state": "lost",
                    "dayNumber": datetime.today().day,
                }
            )

        elif game.force_result_cant_replay:
            logger.info("====== force_result_cant_replay ======")
            if not game.dry_run:
                RefusedLead.objects.create(
                    email=body.get("email"),
                    reason="{'already_play':True, 'game.can_replay':False}",
                )
            return JsonResponse(
                {
                    "state": "cant_replay",
                    "dayNumber": datetime.today().day,
                }
            )

        elif game.force_result_cant_replay_today:
            logger.info("====== force_result_cant_replay_today ======")
            if not game.dry_run:
                RefusedLead.objects.create(
                    email=body.get("email"),
                    reason="{'already_play_today':True, 'game.can_replay':False}",
                )
            return JsonResponse(
                {
                    "state": "cant_replay_today",
                    "dayNumber": datetime.today().day,
                }
            )

        elif game.force_result_won:
            logger.info("====== force_result_won ======")
            # TODO Test that!
            price = Price.objects.get(pk=game.prices.all()[0].id)
            if not game.dry_run:
                code = get_code_price(game)
                unlock_link = f"{DASHBOARD_DNS}/unlock/price/{code}"
                qr_link = generate_qr_price(unlock_link)
                won = WinnedPrice.objects.create(
                    game=game,
                    price=price,
                    price_code=code,
                    unlock_link=unlock_link,
                    price_qrlocation=qr_link,
                )
                lead.price_won = won
                lead.save()
                logger.info("send email ---====--")
                if price.email_template:
                    send_email(game, lead, price, won.price_qrlocation)
                logger.info("email sent =========")
            return JsonResponse(
                {
                    "price": price.id,
                    "displayTitle": price.display_price_name,
                    "offsetTitle": price.offset_price_name,
                    "state": "won",
                    "dayNumber": datetime.today().day,
                }
            )

        if not game.can_replay_today:
            logger.info("====== can't_replay_today ======")
            today = datetime.now().date()
            tomorrow = today + timedelta(1)
            today_start = datetime.combine(today, time())
            today_end = datetime.combine(tomorrow, time())
            already_play = Lead.objects.filter(
                game=game,
                email=body.get("email"),
                creation_date__gte=today_start,
                creation_date__lte=today_end,
            )
            if already_play:
                if not game.dry_run:
                    RefusedLead.objects.create(
                        email=body.get("email"),
                        reason="{'no_more_play_today':True}",
                    )
                logger.info("====== can't_replay_today ======")
                return JsonResponse(
                    {
                        "state": "cant_replay_today",
                        "dayNumber": datetime.today().day,
                    }
                )
        if not game.can_replay:
            logger.info("====== can't replay ======")
            already_play = Lead.objects.filter(
                game=game, email=body.get("email")
            ).count()
            if already_play > 0:
                logger.info("====== already_played ======")
                if not game.dry_run:
                    RefusedLead.objects.create(
                        email=body.get("email"),
                        reason="{'already_play':True, 'game.can_replay':False}",
                    )
                return JsonResponse(
                    {
                        "state": "cant_replay",
                        "dayNumber": datetime.today().day,
                    }
                )

        winner = is_winning(game)
        if not winner:
            logger.info("====== not winner ======")
            return JsonResponse(
                {
                    "state": "lost",
                    "dayNumber": datetime.today().day,
                }
            )
        try:
            price_id, price = get_price(game)
        except Exception as e:
            logger.info(f"====== Get price broken ====== {e}")
            return JsonResponse(
                {
                    "state": "lost",
                    "dayNumber": datetime.today().day,
                }
            )
        logger.info("====== winner ======")
        if not game.dry_run:
            code = get_code_price(game)
            unlock_link = f"{DASHBOARD_DNS}/unlock/price/{code}"
            qr_link = generate_qr_price(unlock_link)
            won = WinnedPrice.objects.create(
                game=game,
                price=price,
                price_code=code,
                unlock_link=unlock_link,
                price_qrlocation=qr_link,
            )
            logger.info("send email ---====--")

        logger.info("email sent =========")
        return JsonResponse(
            {
                "price": price.id,
                "displayTitle": price.display_price_name,
                "offsetTitle": price.offset_price_name,
                "state": "won",
                "dayNumber": datetime.today().day,
            }
        )
