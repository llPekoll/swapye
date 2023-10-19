import logging

from mailjet_rest import Client

from authie.models import MailingInfo

logger = logging.getLogger("app")
import logging


def send_lead(args):
    # logger.info("3 sending email ===============")
    # logger.info("3 sending email ===============")
    mailjet = Client(auth=(args.get("api_key"), args.get("api_secret")), version="v3.1")

    data = {
        "Messages": [
            {
                "From": {
                    "Email": args.get("email_from"),
                    "Name": args.get("display_name"),
                },
                "To": [{"Email": args.get("email_to"), "Name": args.get("name_to")}],
                "TemplateID": args.get("email_template"),
                "TemplateLanguage": True,
                "Subject": args.get("game_name"),
                "Variables": {
                    "name": args.get("price_name"),
                    "qr_location": args.get("qr_location")
                    if args.get("qr_location")
                    else "",
                },
            }
        ]
    }
    # logger.info("sending email")
    ret = mailjet.send.create(data=data)
    return {"body": ret}


def send_email(game, lead, price, qr_location=""):
    try:
        ret = MailingInfo.objects.get(owner=game.owner)
    except MailingInfo.DoesNotExist:
        logger.info("no api key")
        return
    try:
        int(lead.price_won.price.email_template)
    except Exception as e:
        logger.error("template not valid")
        return
    name_to = lead.name if lead.name else "Cher Client"
    payload = {
        "api_key": ret.apikey,
        "api_secret": ret.apipass,
        "email_from": ret.email,
        "display_name": ret.display_name,
        "email_to": lead.email,
        "name_to": name_to,
        "email_template": int(lead.price_won.price.email_template),
        "game_name": game.name,
        "price_name": price.name,
        "qr_location": qr_location,
    }

    # logger.info(payload)
    # try:
    # logger.info(" 1 sending email ===============")
    ret = send_lead(payload)
    # logger.info(" 2 sending email ===============")
    logger.info(ret)
    # except Exception as e:
    # logger.error(f"worker error {e}")
    # return
    # logger.error(f"worker error {e}")
    # return
