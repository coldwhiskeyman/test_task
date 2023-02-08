from datetime import datetime

from pydantic import BaseModel


class Employee(BaseModel):
    """Базовая модель промо"""
    name: str
    email: str
    age: int
    company: str
    join_date: datetime
    job_title: str
    gender: str
    salary: int
