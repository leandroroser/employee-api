import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import (Employees, 
                        Jobs,
                        Departments)
from src.schemas import Base
from src.schemas import (Departments as DepartmentsEntity, 
                         Employees as EmployeesEntity,
                         Jobs as JobsEntity)
from src.connector import Connector
from bulkboto3 import BulkBoto3

local_data_path=os.environ["LOCAL_DATA_PATH"]

MINIO_ENDPOINT=os.environ["MINIO_ENDPOINT"]
MINIO_ACCESS_KEY=os.environ["MINIO_ACCESS_KEY"]
MINIO_SECRET_KEY=os.environ["MINIO_SECRET_KEY"]
TARGET_BUCKET="backup"
NUM_TRANSFER_THREADS = 50
TRANSFER_VERBOSITY = True
 
bulkboto_agent = BulkBoto3(
    resource_type="s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    max_pool_connections=300,
    verbose=TRANSFER_VERBOSITY,
)


def read_csv_file(file_path):
    return pd.read_csv(file_path)

def create_table(engine, entity, domain):
    connector = Connector(engine, entity, domain)
    table_name = entity.__name__
    print(f"Reading {table_name}.csv...")
    table = read_csv_file(f"{local_data_path}/{table_name}.csv")
    for _, row in table.iterrows():
        print("--------HERE---------")
        print(row.to_dict())
        record = domain(**row.to_dict())
        connector.write(record)


if __name__ == "__main__":
    user=os.environ["POSTGRES_USER"]
    password=os.environ["POSTGRES_PASSWORD"]
    host=os.environ["POSTGRES_HOST"]
    port=os.environ["POSTGRES_PORT"]
    db=os.environ["POSTGRES_DB"]
    db_uri=f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    print(f"Creating tables in db...")
    Base.metadata.create_all(bind=engine)

    print(f"Data to db...")
    create_table(session, EmployeesEntity, Employees)
    create_table(session, JobsEntity, Jobs)
    create_table(session, DepartmentsEntity, Departments)

    bulkboto_agent.create_new_bucket(bucket_name=TARGET_BUCKET)
    
    print("Done!")