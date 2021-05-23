import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
import pytz

import requests
import logging

from data import config
from utils.db_api.models.bills import Bill


class Payment:
    id: str = None
    customer_id: int = 0
    order_id: int = 0
    amount: int = 0
    comment: str = ""
    minutes: int = 15
    date_expire: datetime

    def __init__(self, bill: Bill = None, **kwargs):
        if bill:
            self.id = bill.uid
            self.customer_id = bill.customer_id
            self.order_id = bill.order_id
            self.amount = bill.amount
            self.comment = bill.comment
            self.date_expire = bill.date_expire

    # https://developer.qiwi.com/en/p2p-payments/#http
    # https://github.com/QIWI-API/p2p-payments-docs/blob/master/p2p-payments_en.html.md
    HEADERS_JSON = {
        "Authorization": "Bearer " + config.QIWI_SECRET_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    BASE_URL = "https://api.qiwi.com/partner/bill/v1/bills/"

    INVOICE_JSON = {
        "amount": {
            "currency": "RUB",
            "value": "",
        },
        "expirationDateTime": "",
        "comment": "",
        "customer": {"account": ""},
        "customFields": {},
    }

    def create(self):
        """Method to initiate invoice.
        https://developer.qiwi.com/en/p2p-payments/#API
        :param bill_id: bill id
        :type bill_id: str (200)
        :param amount: bill amount in rubbles
        :type amount: float/int/str
        :param comment: comment to the bill
        :type comment: str (255)
        :param email: customer email
        :type email: str
        :param minutes: invoice due period (in minutes)
        :type minutes: int
        :return: payment url or 'error'
        :rtype: str
        """

        invoice_json = self.INVOICE_JSON
        if self.comment is not None:
            invoice_json["comment"] = self.comment
        if self.customer_id is not None:
            invoice_json["customer"]["account"] = str(self.customer_id)

        invoice_json["amount"]["value"] = "{:.2f}".format(self.amount)

        # This invoice is valid for X minutes, adjust accordingly
        local = pytz.timezone('Europe/Moscow')
        date_expire = local.localize(self.date_expire)
        invoice_json["expirationDateTime"] = (
                date_expire
        ).isoformat(sep="T", timespec="seconds")

        url = self.BASE_URL + str(self.id)
        headers = self.HEADERS_JSON
        try:
            invoice_response = requests.put(
                url,
                json=invoice_json,
                headers=headers,
                timeout=15
            )
            cod = invoice_response.status_code
            invoice_data = invoice_response.json()
            if cod == 200:
                return invoice_data["payUrl"]
            else:
                levent = 'qiwi server error (create bill). code - ' + str(cod) + ', response - ' + str(
                    invoice_data)
                logging.warning(levent)
                return 'error'

        except Exception as e:
            levent = 'protocol error (create bill): ' + str(e)
            logging.error(levent)
            return 'error'

    @classmethod
    def payment_confirmation(cls, bill: Bill):
        """Receive payment confirmation.
        https://developer.qiwi.com/en/p2p-payments/#invoice-status
        Statuses:
        =====================================================
        Status   Description                            Final
        WAITING  Invoice issued awaiting for payment    -
        PAID     Invoice paid                           +
        REJECTED Invoice rejected by customer           +
        EXPIRED  Invoice expired. Invoice not paid      +
        :param bill_id: bill id
        :type bill_id: str
        :return: response status value or 'error'
        :rtype: str
        """

        try:
            response = requests.get(
                cls.BASE_URL + str(bill.uid),
                headers=cls.HEADERS_JSON,
                timeout=15
            )
            cod = response.status_code
            res = response.json()
            if cod == 200:
                status = res.get("status")
                return status.get("value")
            else:
                levent = ("qiwi server error (bill status). code - " +
                          str(cod) + ", response - " + str(res))
                logging.warning(levent)
                return 'error'

        except Exception as e:
            levent = "protocol error (bill status): " + str(e)
            logging.error(levent)
            return "error"

    @classmethod
    def payment_cancellation(cls, bill: Bill):
        """Cancel the invoice.
        https://developer.qiwi.com/en/p2p-payments/#cancel
        Statuses:
        =====================================================
        Status   Description                            Final
        WAITING  Invoice issued awaiting for payment    -
        PAID     Invoice paid                           +
        REJECTED Invoice rejected by customer           +
        EXPIRED  Invoice expired. Invoice not paid      +
        :param bill_id: bill id
        :type bill_id: str
        :return: response status value or 'error'
        :rtype: str
        """

        try:
            response = requests.get(
                cls.BASE_URL + str(bill.id) + "/reject",
                headers=cls.HEADERS_JSON,
                timeout=15
            )
            cod = response.status_code  # getting 40X all the time
            res = response.json()
            if cod == 200:
                status = res.get("status")
                return status.get("value")
            else:
                levent = ("qiwi server error (bill status). code - " +
                          str(cod) + ", response - " + str(res))
                logging.warning(levent)
                return 'error'

        except Exception as e:
            levent = "protocol error (bill status): " + str(e)
            logging.error(levent)
            return "error"
