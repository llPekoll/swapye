import logging

from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from backend.settings import AWS_CDN_URL
from games.models import ExtraGameLanguage, Game, GameTrads, PricesTrads

from .models import Icon, Img, RequestedElementDefault, Trad

logger = logging.getLogger("app")


def get_trad(request, lang, section):
    trads = (
        Trad.objects.using("trad")
        .filter(section__name__contains=section)
        .values(f"{lang}_content", f"{lang}_content_rich", "key")
    )
    common_trads = (
        Trad.objects.using("trad")
        .filter(section__name__contains="common")
        .values(f"{lang}_content", f"{lang}_content_rich", "key")
    )
    icons = Icon.objects.using("trad").values("link", "key")
    imgs = Img.objects.using("trad").values("screenshot", "key")
    trads_dict = {jose["key"]: jose[f"{lang}_content"] for jose in trads}
    trads_dict.update(
        {f"{jose['key']}_rich": jose[f"{lang}_content_rich"] for jose in trads}
    )
    trads_dict.update({jose["key"]: jose[f"{lang}_content"] for jose in common_trads})
    trads_dict.update(
        {f"{jose['key']}_rich": jose[f"{lang}_content_rich"] for jose in common_trads}
    )
    trads_dict.update({jose["key"]: jose["link"] for jose in icons})
    trads_dict.update(
        {jose["key"]: f"{AWS_CDN_URL}/{jose['screenshot']}" for jose in imgs}
    )

    return JsonResponse(trads_dict)


def game_trads(request, emblem: str):
    game = get_object_or_404(Game, emblem=emblem)
    extras = ExtraGameLanguage.objects.filter(game=game, is_active=True)
    trad_pack = {}
    for extra in extras:
        trads1 = [
            {
                "openingText": trad.opening_text,
                "closingText": trad.closing_text,
            }
            for trad in GameTrads.objects.filter(extra_game_language=extra)
        ]
        if not trads1:
            trads1 = [
                {
                    "openingText": game.opening_text,
                    "closingText": game.closing_text,
                }
            ]
        trads2 = [
            {
                "name": price.name,
                "img": price.img,
                "priceId": price.price.id,
            }
            for price in PricesTrads.objects.filter(extra_game_language=extra)
        ]
        trads3 = [
            model_to_dict(trad)
            for trad in RequestedElementDefault.objects.using("trad").filter(
                lang=extra.lang
            )
        ]
        trads3 = {trad["key"]: trad["value"] for trad in trads3}
        trad_pack[extra.lang] = {
            "tradDefaults": trads3,
            "tradIntroOutro": trads1,
            "tradPrices": trads2,
            "langs": [extra.lang for extra in extras],
        }

    return JsonResponse(trad_pack)


def game_langs(request, emblem: str):
    game = get_object_or_404(Game, emblem=emblem)
    extras = ExtraGameLanguage.objects.filter(game=game, is_active=True)
    return JsonResponse([extra.lang for extra in extras], safe=False)
