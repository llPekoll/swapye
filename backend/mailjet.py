import os

from mailjet_rest import Client

api_key = "e9ddc06ec93dc7db3fab515c4537fc80"
api_secret = "d6cd862f8916c80ea0a67aa3a009bb68"
# api_key = "34e86d8d6fb4c60b17981eeca7b20bcc"
# api_secret = "0ec14d2b9e41d2d5a1396d9acbcd4326"

mailjet = Client(auth=(api_key, api_secret), version="v3.1")
data = {
    "Messages": [
        {
            "From": {"Email": "paul@swapye.com", "Name": "Paul de Swapye"},
            "To": [{"Email": "yohann.mepa@gmail.com", "Name": "Yohann PaMe"}],
            "TemplateID": 4406586,
            "TemplateLanguage": True,
            "Subject": "Forgotten email",
        }
    ]
}
result = mailjet.send.create(data=data)
logger.info(result.status_code)
logger.info(result.json())
