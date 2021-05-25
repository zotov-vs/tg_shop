from utils.db_api.database import TimedBaseModel, db


class Form(TimedBaseModel):
    __tablename__ = "forms"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customers.id'))

    phone_number = db.Column(db.String)
    phone_region = db.Column(db.String)
    phone_operator = db.Column(db.String)
    phone_old_operator = db.Column(db.String)

    birthday = db.Column(db.Date)
    entity_type_id = db.Column(db.Integer, db.ForeignKey('entities_types.id'))
    number = db.Column(db.String)

    issued_code = db.Column(db.String)
    issued_by = db.Column(db.String)
    issued_date = db.Column(db.Date)

    registration_address = db.Column(db.String)

    foto_main = db.Column(db.String)
    foto_registration = db.Column(db.String)
