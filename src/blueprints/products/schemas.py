import decimal
import typing

from pydantic import BaseModel, condecimal, validator
from sanic import exceptions


class ProductCreateSchema(BaseModel):
    name: str
    description: str
    price: condecimal(max_digits=8, decimal_places=2)

    @validator("name")
    def empty_name(cls, name):
        if not name:
            raise exceptions.BadRequest("Name cannot be empty")
        return name

    @validator("description")
    def empty_description(cls, description):
        if not description:
            raise exceptions.BadRequest("Description cannot be empty")
        return description

    @validator("price")
    def non_positive_price(cls, price):
        if price <= 0:
            raise exceptions.BadRequest("Price must be positive")
        return price


class ProductUpdateSchema(ProductCreateSchema):
    name: typing.Optional[str] = None
    description: typing.Optional[str] = None
    price: condecimal(max_digits=8, decimal_places=2) = None
