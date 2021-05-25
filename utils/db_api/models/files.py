import mimetypes

from asyncpg import UniqueViolationError
from sqlalchemy import sql

from utils.db_api.database import TimedBaseModel, BaseModel, db
from data.config import S3_ACCESS_KEY, S3_SECRET_KEY, S3_URL, S3_BUCKET

import boto3

s3_client = boto3.client(
    service_name='s3',
    endpoint_url=S3_URL,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,

)


class File(TimedBaseModel):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customers.id'), nullable=False)
    file_key = db.Column(db.String, unique=True, nullable=False)
    mime_type = db.Column(db.String, nullable=False, default='')

    query: sql.Select

    @classmethod
    async def add(cls, customer_id: customer_id, file_name: str, file_unique_id,
                  mime_type: str = None, file_prefix: str = ''):
        try:

            file_extension = mimetypes.guess_extension(mime_type)
            file_key = f"{file_prefix}{customer_id}/{file_unique_id}{file_extension}"

            obj = await cls.query.where(cls.file_key == file_key).gino.first()
            if not obj:
                s3_client.upload_file(file_name, S3_BUCKET, file_key)
                obj = cls(customer_id=customer_id, file_key=file_key, mime_type=mime_type)
                await obj.create()
        except UniqueViolationError:
            obj = await cls.query.where(cls.file_key == file_key).gino.first()

        return obj
