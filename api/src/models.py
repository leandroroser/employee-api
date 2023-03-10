from typing import Optional,Dict,Any
#from pydantic import BaseModel
from datetime import datetime
from pydantic_avro.base import AvroBase

PayloadDict = Dict[str, Any]

class BaseOrmModel(AvroBase):
    id: Optional[int]
    class Config:
        orm_mode = True

    @property
    def dict_for_model(self) -> PayloadDict:
        return self.dict(by_alias=False)

class Employees(BaseOrmModel):
    name: str
    datetime: datetime
    job_id: int
    department_id: int
    
class Departments(BaseOrmModel):
    department: str
    
class Jobs(BaseOrmModel):
    job: str