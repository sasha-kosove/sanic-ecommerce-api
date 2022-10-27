from sanic import Blueprint, exceptions, response
from sanic_ext import validate
from sanic_jwt import scoped

from blueprints.transactions.models import Transaction
from common.utilities import decode_access_token

from .models import User
from .schemas import UserUpdateSchema

bp = Blueprint("Users", url_prefix="/users")


@bp.get("")
@scoped("admin")
async def get_all_user(request):
    users = await User.all()
    return response.json(
        {
            "users": [
                {
                    "user_id": str(user.uuid),
                    "username": user.username,
                    "is_active": user.is_active,
                    "is_admin": user.is_admin,
                }
                for user in users
            ]
        }
    )


@bp.get("/<user_id:uuid>")
@scoped("admin")
async def get_user(request, user_id):
    user = await User.get_or_none(uuid=user_id)
    if not user:
        raise exceptions.NotFound(f"Could not find user with ID: {user_id}")

    return response.json(
        {
            "user_id": str(user.uuid),
            "username": user.username,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
        }
    )


@bp.patch("/<user_id:uuid>")
@scoped("admin")
@validate(json=UserUpdateSchema)
async def update_user(request, user_id, body):
    user = await User.get_or_none(uuid=user_id)
    if not user:
        raise exceptions.NotFound(f"Could not find user with ID: {user_id}")

    user.update_from_dict(body.dict(exclude_none=True))
    await user.save()

    return response.json(
        {
            "user_id": str(user.uuid),
            "username": user.username,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
        }
    )


@bp.get("/<user_id:uuid>/transactions")
@scoped("admin")
async def get_all_user_transaction(request, user_id):
    user = await User.get_or_none(uuid=user_id)
    if not user:
        raise exceptions.NotFound(f"Could not find user with ID: {user_id}")

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


@bp.get("/<user_id:uuid>/bills")
@scoped("admin")
async def get_all_user_bill(request, user_id):
    user = await User.get_or_none(uuid=user_id)
    if not user:
        raise exceptions.NotFound(f"Could not find user with ID: {user_id}")

    bills = await user.bills
    return response.json(
        {
            "bills": [
                {
                    "bill_id": str(bill.uuid),
                    "balance": bill.balance,
                }
                for bill in bills
            ]
        }
    )


@bp.get("/<token:str>")
async def activate_user(request, token: str):
    payload = decode_access_token(token)
    user_id = payload.get("user_id")
    user = await User.get_or_none(uuid=user_id)
    if not user:
        raise exceptions.NotFound(f"Requested URL not found")

    user.is_active = True
    await user.save()

    return response.json(
        {
            "success": True,
            "message": "Your account has been activated. You may login to traces",
        }
    )
