import sanic_jwt
from sanic import Blueprint, exceptions, response
from sanic_ext import validate

from blueprints.users.models import User
from blueprints.users.schemas import UserSignInSchema, UserSignUpSchema
from common import utilities

bp = Blueprint("Auth", url_prefix="")


@bp.post("/signup")
@validate(json=UserSignUpSchema)
async def sign_up(request, body: UserSignUpSchema):
    exists_user = await User.get_or_none(username=body.username)

    if exists_user:
        raise exceptions.BadRequest("User already exists.")

    hashed_password = utilities.get_password_hash(body.password1)

    if body.username == "admin":
        user = await User.create(
            username=body.username,
            password=hashed_password,
            is_active=True,
            is_admin=True,
        )

        return response.json(
            {
                "success": True,
                "message": "Registration completed",
            }
        )

    user = await User.create(username=body.username, password=hashed_password)

    token = utilities.create_access_token({"user_id": str(user.uuid)})

    return response.json(
        {
            "success": True,
            "activation_url": f"http://127.0.0.1:8000/api/users/{token}",
            "message": "Registration completed",
        }
    )


@validate(json=UserSignInSchema)
async def authenticate(request, body, *args, **kwargs):
    user = await User.get_or_none(username=body.username)

    if not (user and utilities.verify_password(body.password, user.password)):
        raise sanic_jwt.exceptions.AuthenticationFailed(
            "Incorrect username or password."
        )

    if not user.is_active:
        raise sanic_jwt.exceptions.AuthenticationFailed("Account is not active")

    return user


async def retrieve_user(request, payload, *args, **kwargs):
    if not payload:
        return None
    user_id = payload.get("user_id", None)
    user = await User.get_or_none(id=user_id)
    return user


async def add_scopes_to_payload(user, *args, **kwargs):
    if user.is_admin:
        return "admin"
    if user.is_active:
        return "user"
    return None
