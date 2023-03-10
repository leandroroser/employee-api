from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseSchema(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
class Departments(BaseSchema):
    __tablename__ = "departments"
    department = Column(String, index=True)

class Jobs(BaseSchema):
    __tablename__ = "jobs"
    job = Column(String, index=True)

class Employees(BaseSchema):
    __tablename__ = "employees"
    name = Column(String, index=True)
    datetime = Column(String, index=True)
    department_id = Column(Integer)
    job_id = Column(Integer)
