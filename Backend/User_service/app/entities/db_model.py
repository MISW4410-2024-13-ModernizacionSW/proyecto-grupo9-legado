from datetime import datetime,date
from enum import Enum
from typing import Optional, Union
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field as PField
from sqlalchemy import Column, String
from sqlalchemy_utils import ChoiceType
from sqlmodel import SQLModel, Field

class RolEnum(str, Enum):
    SUPER_ADMINISTRADOR = "Super_Administrador"
    ADMINISTRADOR = "Administrador"
    

class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default=uuid4(), primary_key=True)
    username: str = Field(unique=True)
    fullName: str
    pinCode: str
    password: str
    salt: str
    token: Optional[UUID] = None
    rol: RolEnum = Field(
        sa_column=Column(
            ChoiceType(RolEnum, impl=String()),
            nullable=False,
            default=RolEnum.ADMINISTRADOR,
        )
    )
    expireAt: Optional[datetime] = None
    createdAt: datetime = Field(default=datetime.utcnow())
    updateAt: datetime = Field(default=datetime.utcnow())

class UserCreateIn(BaseModel):
    username: str = PField(pattern=r"^[a-zA-Z0-9]+$")
    fullName: str
    pinCode: str
    password: str
    rol: Optional[RolEnum] = None

class UserCreateOut(BaseModel):
    id: UUID
    createdAt: datetime

class UserUpdateIn(BaseModel):
    rol: Optional[RolEnum] = None
    fullName: Optional[str] = None

class UserAuthIn(BaseModel):
    username: str
    password: str

class UserAuthOut(BaseModel):
    id: UUID
    token: UUID
    expireAt: datetime
  
class UserMeOut(BaseModel):
    id: UUID
    username: str
    fullName: str
    rol: RolEnum
