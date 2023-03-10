from typing import Optional,Dict,Any
#from pydantic import BaseModel
from datetime import datetime
from pydantic_avro.base import AvroBase

PayloadDict = Dict[str, Any]

class BaseOrmModel(AvroBase):
    class Config:
        orm_mode = True

    @property
    def dict_for_model(self) -> PayloadDict:
        return self.dict(by_alias=False)

class Employees(BaseOrmModel):
    id: Optional[int]
    name: str
    datetime: datetime
    job_id: int
    department_id: int


class Departments(BaseOrmModel):
    id: Optional[int]
    department: str


class Jobs(BaseOrmModel):
    id: Optional[int]
    job: str