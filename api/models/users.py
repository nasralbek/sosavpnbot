
from datetime import datetime
from pydantic import UUID4, BaseModel

from utils.constants import TransactionStatus



class CreateUserRequest(BaseModel):
    invited_by : int | None

class AddDaysRequest(BaseModel):
    days : int

class UserResponse(BaseModel):
    tg_id: int
    expire_at: datetime
    uuid: UUID4

class TransactionResponse(BaseModel):
    tg_id       : int
    payment_id  : UUID4
    days        : int
    created_at  : datetime
    updated_at  : datetime
    status      : TransactionStatus 
