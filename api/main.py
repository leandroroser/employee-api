from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi.responses import JSONResponse
from datetime import date
from .src.connector import Connector
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import (Employees, 
                        Jobs,
                        Departments)
from src.schemas import (Departments as DepartmentsEntity, 
                         Employees as EmployeesEntity,
                         Jobs as JobsEntity)
from src.connector import Connector
import os
from dotenv import load_dotenv
import pandas as pd


load_dotenv()

user=os.environ["POSTGRES_USER"]
password=os.environ["POSTGRES_PASSWORD"]
host=os.environ["POSTGRES_HOST"]
port=os.environ["POSTGRES_PORT"]
db=os.environ["POSTGRES_DB"]
db_uri=f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI(title="Employee management system")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status", tags=["status"])
def status() -> JSONResponse:
    return {"status": "I am up"}


@app.get("/{table}", tags=["table"])
async def read_table(table: str):
    if table not in ["employees", "departments", "jobs"]:
        raise HTTPException(status_code=404, detail="Table not found")
    table = table.capitalize()
    connector = Connector(session, globals()[table + "Entity"], globals()[table])
    rows = connector.read_all()
    return rows

@app.post("/{table}", tags=["table"])
async def create_table(table: str, rows: List[dict]):
    if table not in ["employees", "departments", "jobs"]:
        raise HTTPException(status_code=404, detail="Table not found")
    if not 0 < len(rows) <= 1000:
        raise HTTPException(status_code=400, detail="Invalid batch size")
    table = table.capitalize()
    connector = Connector(session, globals()[table + "Entity"], globals()[table])
    connector.write(rows)

"""
@app.put("/{table}", tags=["table"])
async def put_table(table: str, rows: List[dict]):
    raise HTTPException(status_code=405, detail="Not allowed response")


@app.delete("/{table}", tags=["table"])
async def delete_table(table: str, rows: List[dict]):
    raise HTTPException(status_code=405, detail="Not allowed response")
"""

@app.get("/restore_data/{table}/{date}")
async def restore_data(table: str, date: str):
    if table not in ["employees", "departments", "jobs"]:
        raise HTTPException(status_code=404, detail="Table not found")
    table = table.capitalize()
    connector = Connector(session, globals()[table + "Entity"], globals()[table])
    connector.restore_from_avro(table, date, globals()[table + "Entity"], globals()[table])
    return {"message": f"{table} data for {date} has been restored successfully"}

@app.get("/counts_quarter")
async def counts_quarter():
    employees = pd.read_sql_query('select * from Employees',con=engine)
    jobs = pd.read_sql_query('select * from Jobs',con=engine)
    departments = pd.read_sql_query('select * from Departments',con=engine)
    employees["datetime"] = pd.to_datetime(employees.datetime)
    employees["quarter"] = employees.datetime.dt.quarter
    employees = employees.loc[employees.datetime.dt.year == 2021, :]
    merged = employees.merge(departments, left_on="department_id", right_on="id")
    merged = merged.merge(jobs, left_on="job_id", right_on="id")
    merged = pd.concat([merged.loc[:, ["department", "job"]], pd.get_dummies(merged["quarter"])], axis=1)
    merged = merged.groupby(["department", "job"]).sum().reset_index()
    merged = merged.sort_values(["department", "job"])
    return merged.to_json(orient="records")

@app.get("/higher_than_average")
async def counts_quarter():
    employees = pd.read_sql_query('select * from Employees',con=engine)
    jobs = pd.read_sql_query('select * from Jobs',con=engine)
    departments = pd.read_sql_query('select * from Departments',con=engine)
    employees["datetime"] = pd.to_datetime(employees.datetime)
    employees = employees.loc[employees.datetime.dt.year == 2021, :]
    merged = employees.merge(departments, left_on="department_id", right_on="id")
    merged = merged.merge(jobs, left_on="job_id", right_on="id")
    result= merged.loc[:, ["department_id", "department"]]
    result = result.groupby("department").value_counts().reset_index()
    result.columns = ["department", "id", "total"]
    return result.loc[result.total > result.total.mean(), :].to_json(orient="records")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)