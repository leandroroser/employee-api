from sqlalchemy.orm import Session
from typing import Type, List,TypeVar,Generic
from .models import BaseOrmModel
from .schemas import Base
from fastavro import reader, parse_schema
from io import BytesIO
from minio import Minio
from datetime import date
from sqlalchemy.orm import declarative_base


BaseT = TypeVar("BaseT", bound=Base)
BaseOrmModelT = TypeVar("BaseOrmModelT", bound=BaseOrmModel)

class Connector(Generic[BaseT, BaseOrmModelT]):
    def __init__(self, db_session: Session, entity: Base, domain:BaseOrmModel):
        self.db_session = db_session
        self.entity = entity
        self.domain = domain

    def to_domain(self, obj: BaseOrmModel) -> Type[BaseT]:
        return self.entity(**obj.dict())

    def from_domain(self, obj: Base) -> Type[BaseOrmModelT]:
        return BaseOrmModel.from_orm(obj)

    def write(self, obj: BaseOrmModelT):
        db_obj = self.mapper.to_domain(obj)
        self.db_session.add(db_obj)
        self.db_session.commit()

    def read_all(self) -> List[BaseOrmModelT]:
        db_objs = self.db_session.query(self.model).all()
        return [self.mapper.from_domain(db_obj) for db_obj in db_objs]

    def read_by_id(self, id: int) -> BaseOrmModelT:
        db_obj = self.db_session.query(self.model).filter_by(id=id).first()
        return self.mapper.from_domain(db_obj) if db_obj else None

    def update(self, obj: BaseOrmModelT):
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