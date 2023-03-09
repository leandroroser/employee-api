import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from api.src.models import Employee, Job, Department
from api.src.schema import Base
from api.src.connector import Connector

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

    create_tables(connector)
    create_table(connector, "employee", Employee)
    create_table(connector, "job", Job)
    create_table(connector, "department", Department)

    print("Done!")