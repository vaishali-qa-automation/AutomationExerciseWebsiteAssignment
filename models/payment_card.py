from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentCard:
    name: str
    number: str = "12345678"
    cvc: str = "888"
    expiry_month: str = "07"
    expiry_year: str = "2033"