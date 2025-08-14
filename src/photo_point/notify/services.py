import os

import requests
from django.conf import settings
from django.core.mail import send_mail


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
    """
    Отправка SMS через smsc.ru/sys/send.php
    Документация: https://smsc.ru/api/http/
    """
    if not phone:
        raise SendError("Телефон для SMS не указан.")
    if not message:
        raise SendError("Текст сообщения пуст.")

    login = getattr(settings, "SMSC_LOGIN", os.getenv("SMSC_LOGIN"))
    password = getattr(settings, "SMSC_PASSWORD", os.getenv("SMSC_PASSWORD"))
    url = getattr(settings, "SMSC_URL", "https://smsc.ru/sys/send.php")

    if not (login and password):
        raise SendError("SMSC_LOGIN/SMSC_PASSWORD не настроены.")

    params = {
        "login": login,
        "psw": password,
        "phones": phone,
        "mes": message,
    }

    try:
        resp = requests.post(url, data=params, timeout=10)
    except requests.RequestException as e:
        raise SendError(f"Ошибка сети при обращении к SMSC: {e}")

    if not resp.ok:
        raise SendError(f"SMSC HTTP {resp.status_code}: {resp.text[:200]}")

    try:
        data = resp.json()
    except ValueError:
        text = resp.text.strip()
        if "error" in text.lower():
            raise SendError(f"SMSC error: {text[:200]}")
        return "SMS отправлено"

    if data.get("error") or data.get("error_code"):
        code = data.get("error_code")
        err = data.get("error") or "Неизвестная ошибка"
        raise SendError(f"SMSC ошибка {code}: {err}")

    sms_id = data.get("id")
    cnt = data.get("cnt")
    return f"SMS отправлено (id={sms_id}, cnt={cnt})"


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
