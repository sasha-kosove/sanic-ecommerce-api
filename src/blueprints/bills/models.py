import uuid

from tortoise import Model, fields

from blueprints.users.models import User


class Bill(Model):
    id = fields.IntField(pk=True)
    uuid = fields.UUIDField(default=uuid.uuid4)
    balance = fields.DecimalField(max_digits=8, decimal_places=2, default=0)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", on_delete=fields.CASCADE, related_name="bills"
    )
