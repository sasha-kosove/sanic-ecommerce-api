from uuid import UUID

from sanic import Blueprint, exceptions, response
from sanic_ext import validate
from sanic_jwt import scoped

from .models import Product
from .schemas import ProductCreateSchema, ProductUpdateSchema

bp = Blueprint("Products", url_prefix="/products")


@bp.post("")
@validate(json=ProductCreateSchema)
@scoped("admin")
async def create_product(request, body: ProductCreateSchema):
    product = await Product.create(**body.dict())
    return response.json(
        {
            "product_id": str(product.uuid),
            "name": product.name,
            "description": product.description,
            "price": product.price,
        },
        status=201,
    )


@bp.get("")
@scoped(["user", "admin"], require_all=False)
async def get_all_products(request):
    products = await Product.all()
    return response.json(
        {
            "products": [
                {
                    "product_id": str(product.uuid),
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                }
                for product in products
            ]
        }
    )


@bp.get("/<product_id:uuid>")
@scoped(["user", "admin"], require_all=False)
async def get_product(request, product_id: UUID):
    product = await Product.get_or_none(uuid=product_id)

    if not product:
        raise exceptions.NotFound(f"Could not find product with ID: {product_id}")

    return response.json(
        {
            "product_id": str(product.uuid),
            "name": product.name,
            "description": product.description,
            "price": product.price,
        },
    )


@bp.put("/<product_id:uuid>")
@scoped("admin")
@validate(json=ProductCreateSchema)
async def create_or_update_product(
    request, product_id: UUID, body: ProductCreateSchema
):
    product = await Product.get_or_none(uuid=product_id)
    if product:
        product.update_from_dict(body.dict())
        await product.save()
        status = 200
    else:
        product = await Product.create(**body.dict())
        status = 201

    return response.json(
        {
            "product_id": str(product.uuid),
            "name": product.name,
            "description": product.description,
            "price": product.price,
        },
        status=status,
    )


@bp.patch("/<product_id:uuid>")
@scoped("admin")
@validate(json=ProductUpdateSchema)
async def update_product(request, product_id: UUID, body: ProductUpdateSchema):
    product = await Product.get_or_none(uuid=product_id)

    if not product:
        raise exceptions.NotFound(f"Could not find product with ID: {product_id}")

    product.update_from_dict(body.dict(exclude_none=True))
    await product.save()

    return response.json(
        {
            "product_id": str(product.uuid),
            "name": product.name,
            "description": product.description,
            "price": product.price,
        },
    )


@bp.delete("/<product_id:uuid>")
@scoped("admin")
async def delete_product(request, product_id: UUID):
    product = await Product.filter(uuid=product_id).delete()

    if not product:
        raise exceptions.NotFound(f"Could not find product with ID: {product_id}")

    return response.empty(status=204)
