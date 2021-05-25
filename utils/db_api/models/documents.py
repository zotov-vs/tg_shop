from utils.db_api.database import TimedBaseModel, db


class Document(TimedBaseModel):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customers.id'))

    fio = db.Column(db.String)
    birthday = db.Column(db.Date)
    entity_type_id = db.Column(db.Integer, db.ForeignKey('entities_types.id'))
    number = db.Column(db.String)

    issued_code = db.Column(db.String)
    issued_by = db.Column(db.String)
    issued_date = db.Column(db.Date)

    registration_address = db.Column(db.String)

    foto_main = db.Column(db.String)
    foto_registration = db.Column(db.String)

