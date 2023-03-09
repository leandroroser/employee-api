from typing import Optional
from pydantic import BaseModel


class BaseOrmModel(BaseModel):
    id: Optional[int]

    class Config:
        orm_mode = True

    @property
    def dict_for_model(self) -> PayloadDict:
        return self.dict(by_alias=False)


class Employee(BaseOrmMode):
    name: str
    age: int
    job_id: int
    department_id: int


class Department(BaseOrmMode):
    name: str
    location: str


class Job(BaseOrmMode):
    title: str
    salary: int