from sqlalchemy import sql
from data.localization import currency_symbol

from utils.db_api.database import TimedBaseModel, BaseModel, db

class Product(TimedBaseModel):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    entity_type_id = db.Column(db.Integer, db.ForeignKey('entities_types.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    product_description = db.Column(db.String(1024), nullable=True)
    product_image = db.Column(db.String(1024), nullable=True)
    stock_issue_pattern = db.Column(db.String(1024), nullable=True)

    product_price = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.String(255), default='')

    query: sql.Select

    async def get_children_list(self):
        result = await Product.query.where(Product.parent_id == self.id).gino.all()
        return result

    # Возвращает остаток товара
    async def get_stock(self):
        if entit


    async def get_caption(self):
        result = f'{self.product_name}\n\n'
        if self.product_description:
            result += f'{self.product_description}\n\n'
        if self.product_price:
            result += f'Цена: {self.product_price}{currency_symbol}\n' \
                      f'В наличии: \n' \
                      f'накопительная скидка х%: {currency_symbol}\n' \
                      f'Промокод: {currency_symbol}\n' \
                      f'К оплате: {currency_symbol}\n'

        return result

    @classmethod
    async def get(cls, id: int=0):
        item = await cls.query.where(cls.id == id).gino.first()
        return item




