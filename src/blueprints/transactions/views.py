from sanic import Blueprint, Sanic, exceptions, response
from sanic_ext import validate
from sanic_jwt import inject_user, scoped

from blueprints.bills.models import Bill
from common.utilities import encode_transaction_signature, send_webhook

from .models import Transaction
from .schemas import TransactionCreateSchema

bp = Blueprint("Transactions", url_prefix="/transactions")


@bp.post("")
@scoped(["user", "admin"], require_all=False)
@inject_user()
@validate(json=TransactionCreateSchema)
async def create_transaction(request, user, body):
    bill = await Bill.get_or_none(uuid=body.bill_id)

    if not bill:
        bill = await Bill.create(uuid=body.bill_id, user=user)
    else:
        bill_owner = await bill.user

        if bill_owner.uuid != user.uuid:
            raise exceptions.BadRequest(
                f"User with ID:{user.uuid} does not own bill with ID:{body.bill_id}."
            )

    transaction = await Transaction.create(bill=bill)

    app = Sanic.get_app()
    key = f"{app.config.TRANSACTION_PRIVATE_KEY}:{transaction.uuid}:{user.uuid}:{body.bill_id}:{body.amount}"
    signature = encode_transaction_signature(key)

    webhook_body = {
        "signature": signature,
        "transaction_id": str(transaction.uuid),
        "user_id": str(user.uuid),
        "bill_id": str(body.bill_id),
        "amount": str(body.amount),
    }

    webhook_response = await send_webhook(webhook_body)
    webhook_response_json = await webhook_response.json()
    webhook_status = webhook_response.status

    return response.json(webhook_response_json, status=webhook_status)


@bp.get("")
@scoped(["user", "admin"], require_all=False)
@inject_user()
async def get_all_transaction(request, user):
    bills = await user.bills
    data = {"transactions": []}

    for bill in bills:
        transactions = await Transaction.filter(bill=bill)
        data["transactions"].extend(
            [
                {
                    "transaction_id": str(transaction.uuid),
                    "amount": transaction.amount,
                    "bill_id": str(bill.uuid),
                }
                for transaction in transactions
            ]
        )

    return response.json(data)
