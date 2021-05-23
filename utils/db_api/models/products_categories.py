from sqlalchemy import sql

from utils.db_api.database import TimedBaseModel, BaseModel, db


class ProductsCategories(BaseModel):
    __tablename__ = 'products_categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))

    query: sql.Select