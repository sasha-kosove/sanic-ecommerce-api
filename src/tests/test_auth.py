import urllib.parse

from sanic import Sanic


def test_signup(test_client: Sanic):
    request, response = test_client.post(
        "/api/signup",
        json={"username": "user", "password1": "user", "password2": "user"},
    )
    assert response.status == 200
    activation_url = response.json["activation_url"]
    parsed_url = urllib.parse.urlparse(activation_url)
    request, response = test_client.get(parsed_url.path)
    assert response.status == 200
    assert response.json["success"]


def test_signup_invalid_credentials(test_client: Sanic):
    request, response = test_client.post(
        "/api/signup",
        json={"username": "", "password1": "user", "password2": "user"},
    )
    assert response.status == 400

    request, response = test_client.post(
        "/api/signup",
        json={"username": "user", "password1": "", "password2": ""},
    )
    assert response.status == 400

    request, response = test_client.post(
        "/api/signup",
        json={"username": "user", "password1": "user", "password2": "admin"},
    )
    assert response.status == 400


def test_signup_exists_user(test_client: Sanic):
    request, response = test_client.post(
        "/api/signup",
        json={"username": "user", "password1": "user", "password2": "user"},
    )
    assert response.status == 400


def test_signin(test_client: Sanic, data: dict):
    request, response = test_client.post(
        "/api/signin",
        json={"username": "user", "password": "user"},
    )
    data["user_token"] = response.json["access_token"]
    assert response.status == 200


def test_signin_not_exist_user(test_client: Sanic, data: dict):
    request, response = test_client.post(
        "/api/signin",
        json={"username": "fakeuser", "password": "fakeuser"},
    )
    assert response.status == 401


def test_signin_without_activate_account(test_client: Sanic):
    request, response = test_client.post(
        "/api/signup",
        json={
            "username": "unactive_user",
            "password1": "unactive_user",
            "password2": "unactive_user",
        },
    )
    assert response.status == 200

    request, response = test_client.post(
        "/api/signin",
        json={"username": "unactive_user", "password": "unactive_user"},
    )
    assert response.status == 401


def test_signin_admin(test_client: Sanic, data: dict):
    request, response = test_client.post(
        "/api/signup",
        json={"username": "admin", "password1": "admin", "password2": "admin"},
    )

    request, response = test_client.post(
        "/api/signin",
        json={"username": "admin", "password": "admin"},
    )
    data["admin_token"] = response.json["access_token"]
    assert response.status == 200
