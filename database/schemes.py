from typing import Optional, Text
from pydantic import BaseModel
from database.models import UserRole


class UserData(BaseModel):
    username: str
    password: str
    role: UserRole
    full_name : Optional[str] = None


class UsersUpdateData(BaseModel):
    id : int
    username : str | None = None
    password : str | None = None
    full_name : str | None = None
    role : UserRole | None = None


class DrugData(BaseModel):
    name: str
    amount: int
    description : Text
    base_price : float
    sell_price: float