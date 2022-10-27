from sanic import Blueprint, exceptions, response
from sanic_jwt import inject_user, scoped

from .models import Bill

bp = Blueprint("Bills", url_prefix="/bills")


@bp.post("")
@scoped(["user", "admin"], require_all=False)
@inject_user()
async def create_bill(request, user):
    bill = await Bill.create(user=user)
    return response.json(
        {
            "bill_id": str(bill.uuid),
            "balance": bill.balance,
        },
        status=201,
    )


@bp.get("")
@scoped(["user", "admin"], require_all=False)
@inject_user()
async def get_all_bill(request, user):
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
