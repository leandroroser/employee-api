from sqlalchemy.orm import Session
from typing import Type, List
from .models import Base
from .schemas import Base as BaseSchema
from abc import ABC, abstractmethod
from fastavro import reader, parse_schema
from io import BytesIO
from minio import Minio
from datetime import date
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class BaseSchema(BaseModel):
    class Config:
        orm_mode = True

    @property
    def dict_for_model(self) -> PayloadDict:
        return self.dict(by_alias=False)


BaseT = TypeVar("BaseT", bound=Base)
BaseSchemaT = TypeVar("BaseOrmModelT", bound=BaseSchema)

class Connector(Generic[BaseT, BaseSchemaT]):
    def __init__(self, db_session: Session, entity: Base, domain:BaseSchema):
        self.db_session = db_session
        self.entity = entity
        self.domain = domain

    def to_domain(self, obj: BaseSchema) -> Type[BaseT]:
        return self.entity(**obj.dict())

    def from_domain(self, obj: Base) -> Type[BaseSchemaT]:
        return BaseSchema.from_orm(obj)

    def write(self, obj: BaseSchemaT):
        db_obj = self.mapper.to_domain(obj)
        self.db_session.add(db_obj)
        self.db_session.commit()

    def read_all(self) -> List[BaseSchemaT]:
        db_objs = self.db_session.query(self.model).all()
        return [self.mapper.from_domain(db_obj) for db_obj in db_objs]

    def read_by_id(self, id: int) -> BaseSchemaT:
        db_obj = self.db_session.query(self.model).filter_by(id=id).first()
        return self.mapper.from_domain(db_obj) if db_obj else None

    def update(self, obj: BaseSchemaT):
        db_obj = self.db_session.query(self.model).filter_by(id=obj.id).first()
        if db_obj:
            for key, value in obj.dict(exclude_unset=True).items():
                setattr(db_obj, key, value)
            self.db_session.commit()

    def delete(self, id: int):
        db_obj = self.db_session.query(self.model).filter_by(id=id).first()
        if db_obj:
            self.db_session.delete(db_obj)
            self.db_session.commit()

    def restore_from_avro(self, bucket_name: str, date: date):
        client = Minio("minio:9000", access_key="minio", secret_key="minio", secure=False)
        schema_file_name = f"{self.model.__tablename__}.avsc"
        schema_file = client.get_object(bucket_name, schema_file_name)
        schema = parse_schema(schema_file.read())
        backup_file_name = f"{self.model.__tablename__}_{date}.avro"
        backup_file = client.get_object(bucket_name, backup_file_name)
        buffer = BytesIO(backup_file.read())
        with reader(buffer, parse_schema(schema)) as records:
            for record in records:
                obj = self.mapper.from_domain(self.model(**record))
                self.write(obj)