import uuid

from pydantic import BaseModel, condecimal, validator
from sanic import exceptions


class TransactionCreateSchema(BaseModel):
    bill_id: uuid.UUID
    amount: condecimal(max_digits=8, decimal_places=2)

    @validator("amount")
    def non_positive_price(cls, amount):
        if amount <= 0:
            raise exceptions.BadRequest("Amount must be positive")
        return amount
