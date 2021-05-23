from asyncpg import UniqueViolationError

from utils.db_api.database import BaseModel, db


# Типы сущностей:
class EntityType(BaseModel):
    __tablename__ = "entities_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50), unique=True)
    entity_id = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=False)
    name = db.Column(db.String(150), unique=False)

    @classmethod
    async def add(cls, code: str, name: str = '', entity_id: int = 0):
        try:
            obj = cls(code=code, name=name, entity_id=entity_id)
            await obj.create()
        except UniqueViolationError:
            pass

    @classmethod
    async def get(cls, code: str):
        item = await cls.query.where(cls.code == code.lower()).gino.first()
        return item

    @classmethod
    async def get_all(cls, entity_id: int = 0):
        if entity_id:
            items = await cls.query.where(cls.entity_id == entity_id).gino.all()
        else:
            items = await cls.query.where().gino.all()
        return items
