from typing import List

from notify.sms.backends import get_sms_backend
from notify.sms.backends.base import BaseSmsBackend


class SMSMessage:
    def __init__(self, phone_numbers: List[str], message: str):
        self.phone_numbers = phone_numbers
        self.message = message
        self._backend: BaseSmsBackend = get_sms_backend()

    def send(self):
        self._backend.send_sms(phone_numbers=self.phone_numbers, message=self.message)
