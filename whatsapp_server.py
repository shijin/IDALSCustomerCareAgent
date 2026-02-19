import os
import requests
from requests.auth import HTTPBasicAuth


TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")


def send_whatsapp_message(to_number: str, message: str) -> None:
    """
    Send a WhatsApp message using Twilio REST API.
    """
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM]):
        raise RuntimeError("Twilio environment variables not set")

    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"

    payload = {
        "From": TWILIO_WHATSAPP_FROM,
        "To": to_number,
        "Body": message
    }

    response = requests.post(
        url,
        data=payload,
        auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
        timeout=10
    )

    if response.status_code >= 300:
        raise RuntimeError(
            f"Twilio send failed: {response.status_code} {response.text}"
        )
