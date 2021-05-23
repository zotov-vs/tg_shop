from utils.db_api.database import TimedBaseModel, db


class Stock(TimedBaseModel):
    __tablename__ = "stocks_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.product_id, db.ForeignKey('products.id'))
