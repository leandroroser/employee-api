import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from src.models import Employee, Job, Department
from src.schemas import Base
from src.schemas import (Department as DepartmentSchema, 
                         Employee as EmployeeSchema,
                         Job as JobSchema)

from src.connector import Connector
from data_generator import generate_employee_csv,generate_job_csv,generate_department_csv

def read_csv_file(file_path):
    return pd.read_csv(file_path)

def create_table(engine, entity, schema):
    connector = Connector(engine, entity, schema)
    table_name = entity.__name__
    print(f"Creating {table_name}s...")
    table = read_csv_file(f"data/{table_name}s.csv")
    for _, row in table.iterrows():
        record = table_class(**row.to_dict())
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

    generate_employee_csv(f"./data/{Employee.__name__}.csv")
    generate_job_csv(f"./data/{Employee.__name__}.csv")
    generate_department_csv(f"./data/{Employee.__name__}.csv")

    create_table(engine, Employee, EmployeeSchema)
    create_table(engine, Job, JobSchema)
    create_table(engine, Department, DepartmentSchema)

    print("Done!")