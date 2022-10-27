import uuid

from tortoise import Model, fields


class Product(Model):
    id = fields.IntField(pk=True)
    uuid = fields.UUIDField(default=uuid.uuid4)
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    price = fields.DecimalField(max_digits=8, decimal_places=2)
