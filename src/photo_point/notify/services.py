import os

import requests
from django.conf import settings
from django.core.mail import send_mail

from notify.sms.sms_message import SMSMessage


class SendError(Exception):
    pass


def send_email(subject: str, message: str, to_email: str) -> str:
    if not to_email:
        raise SendError("Email получателя не указан.")
    from_email = (getattr(settings, "DEFAULT_FROM_EMAIL", "") or
                  getattr(settings, "EMAIL_HOST_USER", ""))
    sent = send_mail(subject or "(без темы)", message, from_email, [to_email], fail_silently=False)
    if sent != 1:
        raise SendError("Email не отправлен: неизвестная ошибка.")
    return "Email отправлен"


def send_sms(phone: str, message: str) -> str:
    message = SMSMessage(phone_numbers=[phone], message=message)
    message.send()
    # url = os.getenv("SMS_PROVIDER_URL")
    # token = os.getenv("SMS_PROVIDER_TOKEN")
    # if not phone:
    #     raise SendError("Телефон для SMS не указан.")
    # if not (url and token):
    #     raise SendError("SMS-провайдер не настроен (SMS_PROVIDER_URL/TOKEN).")
    #
    # resp = requests.post(
    #     url,
    #     json={"to": phone, "message": message},
    #     headers={"Authorization": f"Bearer {token}"},
    #     timeout=10,
    # )
    # if not resp.ok:
    #     text = resp.text[:200]
    #     raise SendError(f"SMS HTTP {resp.status_code}: {text}")
    return "SMS отправлено"


def send_telegram(chat_id: str, message: str) -> str:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not chat_id:
        raise SendError("Telegram chat_id не указан.")
    if not token:
        raise SendError("TELEGRAM_BOT_TOKEN не задан.")
    resp = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": message},
        timeout=10,
    )
    try:
        data = resp.json()
    except Exception:
        data = {}
    if not resp.ok or not data.get("ok"):
        desc = data.get("description") or resp.text[:200]
        raise SendError(f"Telegram ошибка: {desc}")
    return "Сообщение отправлено в Telegram"
