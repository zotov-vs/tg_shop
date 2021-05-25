import json

from phonenumbers import NumberParseException

from utils.db_api.database import TimedBaseModel, db
from utils.db_api.models.custumers import Custumer


class Phone(TimedBaseModel):
    __tablename__ = "phones"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customers.id'))

    source_number = db.Column(db.String(150))
    number = db.Column(db.String(50))
    region = db.Column(db.String(100))
    operator = db.Column(db.String(50))
    old_operator = db.Column(db.String(50))

    @classmethod
    async def add(cls, customer_id: int, source_number: str):
        import requests
        from phonenumbers import parse
        try:
            phone_obj = parse(number=source_number, region="RU")
        except NumberParseException.NOT_A_NUMBER:
            return {
                'info': f"Неверный формат номера: <pre>{source_number}</pre>",
                'example': ["+74959898533", "74959898533", "84959898533", "4959898533"]
            }

        url = "http://num.voxlink.ru/get/"

        querystring = {"num": f"+{phone_obj.country_code}{phone_obj.national_number}"}

        payload = ""
        response = requests.request("GET", url, data=payload, params=querystring)
        phone_obj = json.loads(response.text)

        if phone_obj.get('info'):
            return phone_obj.get('info', '') + " - разрешенный формат: " + ", ".join(phone_obj.get('example', ''))
        else:
            obj = cls(customer_id=customer_id, source_number=source_number,
                      number=phone_obj.get('full_num'), region=phone_obj.get('region'),
                      operator=phone_obj.get('operator'), old_operator=phone_obj.get('old_operator'))
            await obj.create()

