from typing import List

from notify.sms.backends.base import BaseSmsBackend
from notify.sms.smsc_api.config import SmscConfig
from notify.sms.smsc_api.errors import SmscApiException
from notify.sms.smsc_api.smsc_api import SMSC


class SmsBackend(BaseSmsBackend):
    """
    SMSC SMS backend class.

    Configuration example.

    Modify your settings.py:
        SMS_SETTINGS = {
            "BACKEND": "notifications.sms.backends.smsc.SmsBackend",
            "OPTIONS": {
                "SMSC_LOGIN": "your_login",  # Login from https://smsc.ru
                "SMSC_PASSWORD": "your_password",  # Password
                "SMSC_DEBUG": False,  # Debug flag
                "SMSC_SENDER": False,  # Sender for message
            }
        }

    For more setting see: `SmscConfig`
    """

    def __init__(self, **options):
        super().__init__(**options)
        config = SmscConfig(**options)
        self.client = SMSC(config=config)

    def send_sms(self, phone_numbers: List[str], message: str):
        try:
            self.client.send_sms(','.join(phone_numbers), message)
        except SmscApiException:
            raise
