from enum import Enum


class NotificationType(str, Enum):
    ORDER = "ORDER"
    PAYMENT = "PAYMENT"
    PROMOTION = "PROMOTION"
    ACCOUNT = "ACCOUNT"