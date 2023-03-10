from sqlalchemy.orm import Session
from typing import Type, List,TypeVar,Generic
from .models import BaseOrmModel
from .schemas import Base
from fastavro import reader, parse_schema
from io import BytesIO
from datetime import date
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

BaseT = TypeVar("BaseT", bound=Base)
BaseOrmModelT = TypeVar("BaseOrmModelT", bound=BaseOrmModel)

MINIO_ENDPOINT=os.environ["MINIO_ENDPOINT"]
MINIO_ACCESS_KEY=os.environ["MINIO_ACCESS_KEY"]
MINIO_SECRET_KEY=os.environ["MINIO_SECRET_KEY"]
TARGET_BUCKET=os.environ["BACKUP_BUCKET"]

s3 = boto3.resource("s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY)


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
        try:
            self.db_session.add(db_obj)
            self.db_session.commit()
        except:
            self.db_session.rollback()
            raise
    
    def write_all(self, obj: List[BaseOrmModelT]):
        for elem in obj:
            self.write(elem)

    def read_all(self) -> List[BaseOrmModelT]:
        db_objs = self.db_session.query(self.entity).all()
        return [self.convert_db_to_domain(db_obj) for db_obj in db_objs]

    def read_by_id(self, id: int) -> BaseOrmModelT:
        db_obj = self.db_session.query(self.entity).filter_by(id=id).first()
        return self.convert_db_to_domain(db_obj) if db_obj else None

    def update(self, obj: BaseOrmModelT):
        db_obj = self.db_session.query(self.entity).filter_by(id=obj.id).first()
        if db_obj:
            try:
                for key, value in obj.dict(exclude_unset=True).items():
                    setattr(db_obj, key, value)
                self.db_session.commit()
            except:
                self.db_session.rollback()
                raise

    def delete(self, id: int):
        db_obj = self.db_session.query(self.entity).filter_by(id=id).first()
        if db_obj:
            try:
                self.db_session.delete(db_obj)
                self.db_session.commit()
            except:
                self.db_session.rollback()
                raise
            
    def delete_all(self, entity: BaseT):
        try:
            self.db_session.query(entity).delete()
            self.db_session.commit()
        except:
            self.db_session.rollback()
            raise

    def restore_from_avro(self, date: str, entity: Base, domain: any):
        schema_file_name = f"{domain.__name__}.avsc"
        schema_file = s3.Object(TARGET_BUCKET, schema_file_name)
        schema_data = schema_file.get()["Body"].read().encode('utf-8')
        schema = parse_schema(schema_data)
        backup_file_name = f"{domain.__name__}_{date}.avro"
        backup_file = s3.Object(TARGET_BUCKET, backup_file_name)
        buffer = BytesIO(backup_file.get()["Body"].read())
        print(f"Deleting table for {domain.__name__}")
        self.delete_all(entity)
        print("Writing data")
        with reader(buffer, schema) as records:
            for record in records:
                domain_obj = domain(**record)
                self.write(domain_obj)
