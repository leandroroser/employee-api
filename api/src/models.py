from typing import Optional,Dict,Any
from pydantic import BaseModel
from datetime import datetime

PayloadDict = Dict[str, Any]

class BaseOrmModel(BaseModel):
    class Config:
        orm_mode = True

    @property
    def dict_for_model(self) -> PayloadDict:
        return self.dict(by_alias=False)


class Employee(BaseOrmModel):
    id: Optional[int]
    name: str
    datetime: datetime
    job_id: int
    department_id: int


class Department(BaseOrmModel):
    id: Optional[int]
    department: str

class Job(BaseOrmModel):
    id: Optional[int]
    job: str