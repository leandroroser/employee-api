from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import JSONResponse
from datetime import date
from schemas import Employee, Department, Job
from app.connector import Connector

description = """
"""

app = FastAPI(title="mployee management system")

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
    if table not in ["employee", "department", "job"]:
        raise HTTPException(status_code=404, detail="Table not found")
    connector = Connector(globals()[table.capitalize()])
    rows = connector.read_all()
    return rows


@app.post("/{table}", tags=["table"])
async def create_table(table: str, rows: List[dict]):
    if table not in ["employee", "department", "job"]:
        raise HTTPException(status_code=404, detail="Table not found")
    if not 0 < len(rows) <= 1000:
        raise HTTPException(status_code=400, detail="Invalid batch size")
    connector = Connector(globals()[table.capitalize()])
    connector.write(rows)

@app.put("/{table}", tags=["table"])
    raise HTTPException(status_code=405, detail="Not allowed response")

@app.delete("/{table}", tags=["table"])
    raise HTTPException(status_code=405, detail="Not allowed response")


@app.get("/restore_data/{table}/{date}")
async def restore_data(table: str, date: date):
    if table not in ["employee", "department", "job"]:
        raise HTTPException(status_code=404, detail="Table not found")
    connector = Connector(globals()[table.capitalize()])
    connector.restore_from_avro(table, date)
    return {"message": f"{table} data for {date} has been restored successfully"}