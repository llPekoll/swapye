import os
import string
import tempfile
from random import choice, choices

import qrcode

from backend import settings
from games.models import Game, WinnedPrice

from .boto import get, push


def get_emblem():
    def tiny_url_generator():
        tiny_string = ""
        for _ in range(9):
            tiny_string += choices(
                population=(
                    choice(string.printable[:10]),
                    choice(string.printable[10:62]),
                ),
                weights=[0.4, 0.6],
                k=8,
            )[0]
        return tiny_string

    emblem = tiny_url_generator()
    is_url_in_base = Game.objects.filter(emblem=f"{emblem}")
    while is_url_in_base:
        emblem = tiny_url_generator()
        is_url_in_base = Game.objects.filter(emblem=emblem)
    return emblem


def get_code_price(game: Game):
    def tiny_url_generator():
        tiny_string = ""
        for _ in range(9):
            tiny_string += choices(
                population=(
                    choice(string.printable[:10]),
                    choice(string.printable[10:62]),
                ),
                weights=[0.4, 0.6],
                k=8,
            )[0]
        return tiny_string

    price_code = tiny_url_generator()
    is_url_in_base = WinnedPrice.objects.filter(
        price_code=price_code, price_taken=True, game=game
    )
    while is_url_in_base:
        emblem = tiny_url_generator()
        is_url_in_base = Game.objects.filter(price_code=price_code)
    return price_code


def generate_qr_price(unlock_link: str):
    if settings.STATE == "TEST":
        return "Http:sadf/sdfa.cmo"
    emblem = unlock_link.split("/")[-1]
    qr = qrcode.make(unlock_link, border=0)
    location = ""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    qr.save(tmp.name)
    location = f"qr/{settings.STATE}/winned_prices/qr_{emblem}.png"
    cdn_location = push(location, "qr", tmp.name)
    os.remove(tmp.name)
    return cdn_location


def generate_qr(tips_link: str):
    if settings.STATE == "TEST":
        return "Http:sadf/sdfa.cmo"
    emblem = tips_link.split("/")[-1]
    qr = qrcode.make(tips_link, border=0)
    location = ""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    qr.save(tmp.name)
    location = f"qr/qr_{emblem}.png"
    cdn_location = push(location, "qr", tmp.name)
    os.remove(tmp.name)
    return cdn_location
