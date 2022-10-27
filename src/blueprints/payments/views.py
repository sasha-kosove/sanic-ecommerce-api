from sanic import Blueprint, Sanic, exceptions, response
from sanic_ext import validate
from sanic_jwt import inject_user, scoped

from blueprints.bills.models import Bill
from blueprints.products.models import Product
from blueprints.transactions.models import Transaction
from common.utilities import encode_transaction_signature

from .schemas import PaymentSchema, TransactionConfirmSchema

bp = Blueprint("Payment", url_prefix="/payment")


@bp.post("/webhook")
@validate(json=TransactionConfirmSchema)
async def confirm_transaction(request, body):
    app = Sanic.get_app()
    key = f"{app.config.TRANSACTION_PRIVATE_KEY}:{body.transaction_id}:{body.user_id}:{body.bill_id}:{body.amount}"
    signature = encode_transaction_signature(key)
    if body.signature != signature:
        raise exceptions.BadRequest("Invalid signature.")

    transaction = await Transaction.get_or_none(uuid=body.transaction_id)
    if not transaction:
        raise exceptions.BadRequest(
            f"Transaction with ID:{body.transaction_id} does not exist."
        )
    transaction.amount = body.amount
    await transaction.save()

    bill = await Bill.get_or_none(uuid=body.bill_id)
    if not transaction:
        raise exceptions.BadRequest(f"Bill with ID:{body.bill_id} does not exist.")
    bill.balance += body.amount
    await bill.save()

    return response.json(
        {"success": True, "message": "Transaction completed."}, status=201
    )


@bp.post("")
@inject_user()
@scoped(["user", "admin"], require_all=False)
@validate(json=PaymentSchema)
async def buy_product(request, user, body):
    bill = await Bill.get_or_none(uuid=body.bill_id)

    if not bill:
        raise exceptions.BadRequest(f"Bill with ID:{body.bill_id} does not exist.")

    bill_owner = await bill.user

    if bill_owner.uuid != user.uuid:
        raise exceptions.BadRequest(
            f"User with ID:{user.uuid} does not own bill with ID:{body.bill_id}."
        )

    product = await Product.get_or_none(uuid=body.product_id)

    if not product:
        raise exceptions.BadRequest(
            f"Product with ID:{body.product_id} does not exist."
        )

    if bill.balance < product.price:
        raise exceptions.BadRequest(f"Insufficient funds on the bill ID:{bill.uuid}.")

    bill.balance -= product.price
    await bill.save()

    return response.json(
        {"success": True, "message": "Purchase completed."}, stasus=201
    )
