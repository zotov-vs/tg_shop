from utils.db_api.database import TimedBaseModel, db
from utils.db_api.models.products import Product


class Stock(TimedBaseModel):
    __tablename__ = "stocks_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.product_id, db.ForeignKey('products.id'))
    product_key = db.Column(db.String(250))

    @classmethod
    async def add(cls, product: Product, product_key: str):
        obj = cls(product_id=product.id, product_keys=product_key)
        obj.create()
        return obj

