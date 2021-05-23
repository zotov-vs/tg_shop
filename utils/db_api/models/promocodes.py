from utils.db_api.database import BaseModel, db


class Promocode(BaseModel):
    __tablename__ = "promocodes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50), unique=True)
    day_expire = db.Column(db.Integer, default=0)
    start = db.Column(db.Date, default='2020-01-01')
    finish = db.Column(db.Date, default='2099-12-31')

    @classmethod
    async def get(cls, code: str):
        item = await cls.query.where(cls.code == code.upper()).gino.first()
        return item
