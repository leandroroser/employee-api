from typing import Optional,Dict,Any
from pydantic import BaseModel

PayloadDict = Dict[str, Any]

class BaseOrmModel(BaseModel):
    id: Optional[int]

    class Config:
        orm_mode = True

    @property
    def dict_for_model(self) -> PayloadDict:
        return self.dict(by_alias=False)


class Employee(BaseOrmModel):
    name: str
    age: int
    job_id: int
    department_id: int


class Department(BaseOrmModel):
    name: str
    location: str


class Job(BaseOrmModel):
    title: str
    salary: int