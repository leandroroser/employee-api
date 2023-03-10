import os
import pandas as pd
from sqlalchemy import create_engine
from src.models import Employee, Job, Department
from src.schemas import Base
from src.schemas import (Department as DepartmentEntity, 
                         Employee as EmployeeEntity,
                         Job as JobEntity)

from src.connector import Connector


local_data_path=os.environ["LOCAL_DATA_PATH"]

def read_csv_file(file_path):
    return pd.read_csv(file_path)

def create_table(engine, entity, domain):
    connector = Connector(engine, entity, domain)
    table_name = entity.__name__
    print(f"Creating {table_name}s...")
    table = read_csv_file(f"{local_data_path}/{table_name}.csv")
    for _, row in table.iterrows():
        record = entity(**row.to_dict())
        connector.write(record)

def create_tables(connector):
    print("Creating Tables...")
    Base.metadata.create_all(bind=connector.db_session.bind)

if __name__ == "__main__":
    user=os.environ["POSTGRES_USER"]
    password=os.environ["POSTGRES_PASSWORD"]
    host=os.environ["POSTGRES_HOST"]
    port=os.environ["POSTGRES_PORT"]
    db=os.environ["POSTGRES_DB"]
    db_uri=f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(db_uri)

    print(f"Data to db...")
    create_table(engine, EmployeeEntity, Employee)
    create_table(engine, JobEntity, Job)
    create_table(engine, DepartmentEntity, Department)

    print("Done!")