from pydantic import BaseModel
from enum import Enum as pydanticEnum
from datetime import date


class TransactionType(str, pydanticEnum):
    revenue = 'revenue'
    expenses = 'expenses'

class BaseTransaction(BaseModel):
    user_id: str
    category_id: int
    amount: float
    t_description: str
    t_type: TransactionType
    t_date: date

class CreateTransaction(BaseTransaction):
    pass

class UpdateTransaction(BaseTransaction):
    transactions_id: int


class TransactionRead(BaseTransaction):
    transactions_id: int



