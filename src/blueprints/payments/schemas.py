import uuid

from pydantic import BaseModel

from blueprints.transactions.schemas import TransactionCreateSchema


class TransactionConfirmSchema(TransactionCreateSchema):
    signature: str
    transaction_id: uuid.UUID
    user_id: uuid.UUID


class PaymentSchema(BaseModel):
    product_id: uuid.UUID
    bill_id: uuid.UUID
