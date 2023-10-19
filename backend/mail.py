import os

from mailjet_rest import Client

api_key = "34e86d8d6fb4c60b17981eeca7b20bcc"
api_secret = "0ec14d2b9e41d2d5a1396d9acbcd4326"
mailjet = Client(auth=(api_key, api_secret), version="v3.1")
data = {
    "Messages": [
        {
            "From": {"Email": "comptepayops@gmail.com", "Name": "Yohann"},
            "To": [{"Email": "comptepayops@gmail.com", "Name": "Yohann"}],
            "Subject": "Greetings from Mailjet.",
            "TextPart": "My first Mailjet email",
            "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
            "CustomID": "AppGettingStartedTest",
        }
    ]
}
result = mailjet.send.create(data=data)
print(result.status_code)
print(result.json())
