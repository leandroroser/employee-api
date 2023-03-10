from datetime import datetime
from io import BytesIO
from fastavro import writer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import boto3
from src.connector import Connector
from src.models import Employees, Jobs, Departments
from src.schemas import (Departments as DepartmentsEntity,
                         Employees as EmployeesEntity,
                         Jobs as JobsEntity)

MINIO_ENDPOINT=os.environ["MINIO_ENDPOINT"]
MINIO_ACCESS_KEY=os.environ["MINIO_ACCESS_KEY"]
MINIO_SECRET_KEY=os.environ["MINIO_SECRET_KEY"]
TARGET_BUCKET="backup"
NUM_TRANSFER_THREADS = 50
TRANSFER_VERBOSITY = True
USER = os.environ["POSTGRES_USER"]
PASSWORD = os.environ["POSTGRES_PASSWORD"]
HOST = os.environ["POSTGRES_HOST"]
PORT = os.environ["POSTGRES_PORT"]
DB = os.environ["POSTGRES_DB"]
DB_URI = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
 
    
s3 = boto3.client('s3',
                  aws_access_key_id=MINIO_ACCESS_KEY,
                  aws_secret_access_key=MINIO_SECRET_KEY,
                  endpoint_url=MINIO_ENDPOINT,
                  use_ssl=False)

def backup_to_avro(engine, entity, domain):
    connector = Connector(engine, entity, domain)
    table_name = entity.__name__
    backup_filename = f"{table_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.avro"
    schema_filename = f"{table_name}.avsc"

    data = connector.read_all()
    schema = connector.model.avro_schema()
    data_buffer = BytesIO()
    writer(data_buffer, schema, data)
    data_buffer.seek(0)

    schema_buffer = BytesIO(schema.to_json().encode("utf-8"))
    schema_buffer.seek(0)

    try:
        s3.upload_fileobj(data_buffer, TARGET_BUCKET, backup_filename)
        print(f"Backup of table {table_name} uploaded to MinIO: {TARGET_BUCKET}")

        s3.upload_fileobj(schema_buffer, TARGET_BUCKET, schema_filename)
        print(f"Schema for table {table_name} uploaded to MinIO: {TARGET_BUCKET}")
    except Exception as err:
        print(f"Error uploading backup of table {table_name} to MinIO: {err}")

if __name__ == "__main__":
    print(f"Running backup now: {datetime.now().strftime('%Y-%m-%d_%H-%M')}")

    engine = create_engine(DB_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    backup_to_avro(session, EmployeesEntity, Employees)
    backup_to_avro(session, JobsEntity, Jobs)
    backup_to_avro(session, DepartmentsEntity, Departments)

    print("Backup process completed.")