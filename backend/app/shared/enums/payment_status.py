from enum import Enum


class PaymentStatus(str, Enum):
    INITIATED = "INITIATED"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"