from typing import List, Tuple

from django.shortcuts import render

from .forms import NotificationForm
from .services import send_email, send_sms, send_telegram, SendError


def _order_channels(primary: str, available: List[str]) -> List[str]:
    base = ["email", "sms", "tg"]
    ordered = [primary] + [c for c in base if c != primary]
    seen, result = set(), []
    for c in ordered:
        if c in available and c not in seen:
            result.append(c);
            seen.add(c)
    return result


def notify_view(request):
    form = NotificationForm(request.POST or None)
    attempts: List[Tuple[str, bool, str]] = []
    overall = None

    if request.method == "POST" and form.is_valid():
        cd = form.cleaned_data
        available = []
        if cd.get("email"):
            available.append("email")
        if cd.get("phone"):
            available.append("sms")
        if cd.get("telegram_chat_id"):
            available.append("tg")

        order = _order_channels(cd["primary_channel"], available)

        for ch in order:
            try:
                if ch == "email":
                    msg = send_email(cd.get("subject"), cd["message"], cd.get("email"))
                elif ch == "sms":
                    msg = send_sms(cd.get("phone"), cd["message"])
                else:
                    msg = send_telegram(cd.get("telegram_chat_id"), cd["message"])
                attempts.append((ch, True, msg))
                overall = "success"
                break
            except SendError as e:
                attempts.append((ch, False, str(e)))
            except Exception as e:
                attempts.append((ch, False, f"Неизвестная ошибка: {e}"))

        if overall != "success":
            overall = "failed"

    return render(request, "notify.html", {
        "form": form,
        "attempts": attempts,
        "overall": overall,
    })
