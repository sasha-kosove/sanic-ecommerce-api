from datetime import datetime, timedelta

import aiohttp
import jwt
from Crypto.Hash import SHA1
from passlib.context import CryptContext
from sanic import exceptions

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "c2e1b74dc7392a8692a312a10801994be2b54b2e1fc2f4a02fa4993019b88c21"
ALGORITHM = "HS256"


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=14)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def decode_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.DecodeError:
        raise exceptions.NotFound("Requested URL not found")


def encode_transaction_signature(key):
    h = SHA1.new()
    h.update(f"{key}".encode())
    signature = h.hexdigest()
    return signature


async def send_webhook(body):
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            "http://127.0.0.1:8000/api/payment/webhook", json=body
        )
        return response
