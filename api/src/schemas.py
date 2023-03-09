from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, index=True)

    employees = relationship("Employee", back_populates="department")

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, index=True)

    employees = relationship("Employee", back_populates="job")

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    datetime = Column(String, index=True)
    department_id = Column(Integer, index=True)
    job_id = Column(Integer, index=True)

    department = relationship("Department", back_populates="employees")
    job = relationship("Job", back_populates="employees")