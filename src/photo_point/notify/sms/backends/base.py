from abc import abstractmethod, ABCMeta
from typing import List


class BaseSmsBackend(metaclass=ABCMeta):
    """ Base SMS backend class. """

    def __init__(self, **options):
        pass

    @abstractmethod
    def send_sms(self, phone_numbers: List[str], message: str):
        """ Sends a message to the specified numbers. """
        raise NotImplementedError()
