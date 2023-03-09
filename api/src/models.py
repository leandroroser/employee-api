from typing import Optional
from pydantic import BaseModel


class Employee(BaseModel):
    id: Optional[int]
    name: str
    age: int
    job_id: int
    department_id: int


class Department(BaseModel):
    id: Optional[int]
    name: str
    location: str


class Job(BaseModel):
    id: Optional[int]
    title: str
    salary: int