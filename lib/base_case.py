import uuid
from statuses.operationText import *


class BaseCase:
    @staticmethod
    def creditByAccount(externalRef=None, account=None, amount=None, currency=None, hasFee=None):
        if externalRef is None:
            externalRef = f"{uuid.uuid4()}"
        return {
            "externalRef": f"{externalRef}",
            "receiver": {
                "account": account
            },
            "amount": amount,
            "currency": currency,
            "description": CREDITBYACCOUNT,
            "additionalParams": {
                "hasFee": hasFee
            }
        }

