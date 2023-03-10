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
    def __init__(self, db_session: Session, entity: Type[BaseT], domain: Type[BaseOrmModelT]):
        self.db_session = db_session
        self.entity = entity
        self.domain = domain
        
    def convert_db_to_domain(self, entity: BaseT) -> BaseOrmModelT:
        return self.domain.from_orm(entity)

    def convert_domain_to_db(self, domain: BaseOrmModelT) -> BaseT:
        return self.entity(**domain.dict_for_model)

    def write(self, obj: BaseOrmModelT):
        db_obj = self.convert_domain_to_db(obj)
        self.db_session.add(db_obj)
        self.db_session.commit()

    def read_all(self) -> List[BaseOrmModelT]:
        db_objs = self.db_session.query(self.entity).all()
        return [self.convert_db_to_domain(db_obj) for db_obj in db_objs]

    def read_by_id(self, id: int) -> BaseOrmModelT:
        db_obj = self.db_session.query(self.entity).filter_by(id=id).first()
        return self.convert_db_to_domain(db_obj) if db_obj else None

    def update(self, obj: BaseOrmModelT):
        db_obj = self.db_session.query(self.entity).filter_by(id=obj.id).first()
        if db_obj:
            for key, value in obj.dict(exclude_unset=True).items():
                setattr(db_obj, key, value)
            self.db_session.commit()

    def delete(self, id: int):
        db_obj = self.db_session.query(self.entity).filter_by(id=id).first()
        if db_obj:
            self.db_session.delete(db_obj)
            self.db_session.commit()

    def restore_from_avro(self, bucket_name: str, date: date):
        client = Minio("minio:9000", access_key="minio", secret_key="minio", secure=False)
        schema_file_name = f"{self.entity.__tablename__}.avsc"
        schema_file = client.get_object(bucket_name, schema_file_name)
        schema = parse_schema(schema_file.read())
        backup_file_name = f"{self.entity.__tablename__}_{date}.avro"
        backup_file = client.get_object(bucket_name, backup_file_name)
        buffer = BytesIO(backup_file.read())
        with reader(buffer, parse_schema(schema)) as records:
            for record in records:
                self.write(self.domain(**record))