from django import forms

CHANNELS = (
    ("email", "Email"),
    ("sms", "SMS"),
    ("tg", "Telegram"),
)


class NotificationForm(forms.Form):
    subject = forms.CharField(label="Тема (для Email)", required=False)
    message = forms.CharField(label="Сообщение", widget=forms.Textarea, required=True)

    email = forms.EmailField(label="Email получателя", required=False)
    phone = forms.CharField(label="Телефон (SMS)", required=False)
    telegram_chat_id = forms.CharField(label="Telegram chat_id", required=False)

    primary_channel = forms.ChoiceField(label="Основной канал", choices=CHANNELS, initial="email")
    allow_fallback = forms.BooleanField(
        label="Пробовать другие каналы при сбое", required=False, initial=True
    )

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")
        phone = cleaned.get("phone")
        chat = cleaned.get("telegram_chat_id")
        if not any([email, phone, chat]):
            raise forms.ValidationError("Укажите хотя бы один контакт: Email, Телефон или Telegram chat_id.")
        return cleaned
