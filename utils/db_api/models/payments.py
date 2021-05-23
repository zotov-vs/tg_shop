from sqlalchemy import sql

from utils.db_api.database import TimedBaseModel, BaseModel, db

class Payment(TimedBaseModel):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customers.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True)
    entity_type_id = db.Column(db.Integer, db.ForeignKey('entities_types.id'), nullable=True)
    payments_sum = db.Column(db.Integer)

    query: sql.Select