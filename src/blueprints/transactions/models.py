import uuid

from tortoise import Model, fields

from blueprints.bills.models import Bill


class Transaction(Model):
    id = fields.IntField(pk=True)
    uuid = fields.UUIDField(default=uuid.uuid4)
    amount = fields.DecimalField(max_digits=8, decimal_places=2, default=0)

    bill: fields.ForeignKeyRelation[Bill] = fields.ForeignKeyField(
        "models.Bill", on_delete=fields.CASCADE, related_name="transactions"
    )

    def __str__(self):
        return f"{self.uuid}"
