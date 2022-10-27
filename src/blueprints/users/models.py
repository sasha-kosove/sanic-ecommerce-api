import uuid

from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True)
    uuid = fields.UUIDField(default=uuid.uuid4)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=255)
    is_admin = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=False)

    def __str__(self):
        return str(self.uuid)

    def to_dict(self):
        return {"user_id": self.id, "username": self.username}
