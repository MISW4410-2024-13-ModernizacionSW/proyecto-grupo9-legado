from datetime import datetime,date
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field as PField 
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field
from sqlalchemy_utils import ChoiceType
from enum import Enum

class GenderEnum(str, Enum):
    FEMENINO = "Femenino"
    MASCULINO = "Masculino"
    

class Employe(SQLModel, table=True ):
    id: Optional[UUID] = Field(default=uuid4(), primary_key=True)
    fistName: str 
    surName: str
    dateBirth: date
    gender: GenderEnum = Field(
        sa_column=Column(
            ChoiceType(GenderEnum, impl=String()),
            nullable=False,
            default=GenderEnum.FEMENINO,
        )
    )
    contact: str
    email:str
    addressLine1: str
    addressLine2: str
    noApt: str
    postCode: str
    departament:str
    designation: str
    status: str
    dateHired: date
    basicSalary: int
    JobTitle: str
    image: str


class EmployeCreateIn(BaseModel):
    fistName: str 
    surName: str
    dateBirth: date
    contact: str
    email:str
    addressLine1: str
    addressLine2: str
    noApt: str
    postCode: str
    departament:str
    designation: str
    status: str
    dateHired: date
    basicSalary: int
    JobTitle: str
    image: str

class EmployeCreateOut(BaseModel):
    id: UUID

class EmployeOut(BaseModel):
    id: Optional[UUID]
    contact: str
    email:str
    addressLine1: str
    addressLine2: str
    noApt: str
    postCode: str
    departament:str
    designation: str
    status: str
    dateHired: date
    basicSalary: int
    JobTitle: str
    image: str

class EmployeUpdateIn(BaseModel):
    contact: str
    addressLine1: str
    addressLine2: str
    noApt: str
    postCode: str
    departament:str
    designation: str
    status: str
    basicSalary: int
    JobTitle: str
