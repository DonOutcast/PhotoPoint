from dataclasses import dataclass


@dataclass
class SmscConfig:
    SMSC_LOGIN: str
    SMSC_PASSWORD: str
    SMSC_POST: bool = False
    SMSC_HTTPS: bool = False
    SMSC_DEBUG: bool = False
    SMSC_CHARSET: str = "utf-8"
    SMSC_SENDER: str = False

    SMTP_FROM: str = "api@smsc.ru"
    SMTP_SERVER: str = "send.smsc.ru"
    SMTP_LOGIN: str = ""
    SMTP_PASSWORD: str = ""
