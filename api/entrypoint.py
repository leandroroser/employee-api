import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from src.models import Employee, Job, Department
from src.schemas import Base
from src.connector import Connector
from data_generator import generate_employee_csv,generate_job_csv,generate_department_csv

def read_csv_file(file_path):
    return pd.read_csv(file_path)

def create_table(connector, table_name, table_class):
    print(f"Creating {table_name}s...")
    table = read_csv_file(f"data/{table_name}s.csv")
    for _, row in table.iterrows():
        record = table_class(**row.to_dict())
        connector.write(record)

def create_tables(connector):
    print("Creating Tables...")
    Base.metadata.create_all(bind=connector.db_session.bind)

if __name__ == "__main__":
    db_uri = os.environ["DATABASE_URI"]
    engine = create_engine(db_uri)
    connector = Connector(engine)

    generate_employee_csv("./data/employee.csv")
    generate_job_csv("./data/job.csv")
    generate_department_csv("./data/department.csv")

    create_tables(connector)
    create_table(connector, "employee", Employee)
    create_table(connector, "job", Job)
    create_table(connector, "department", Department)

    print("Done!")