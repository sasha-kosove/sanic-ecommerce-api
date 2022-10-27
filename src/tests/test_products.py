import pytest
from sanic import Sanic


@pytest.mark.parametrize(
    "test_input, expected",
    [("admin_token", 201), ("user_token", 403), ("anonymous_user_token", 401)],
)
def test_add_product(test_client: Sanic, data: dict, test_input, expected):
    data["anonymous_user_token"] = "invalid_token"
    token = data[test_input]
    request, response = test_client.post(
        "/api/products",
        json={"name": "Pencil", "description": "Awesome pensil", "price": 44.44},
        headers={"Authorization": f"Bearer {token}"},
    )
    if test_input == "admin_token":
        data["product_id"] = response.json["product_id"]
    assert response.status == expected


def test_add_product_invalid_data(test_client: Sanic, data: dict):
    token = data["admin_token"]
    request, response = test_client.post(
        "/api/products",
        json={"name": "", "description": "Awesome pensil", "price": 44.44},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 400

    request, response = test_client.post(
        "/api/products",
        json={"name": "Pencil", "description": "", "price": 44.44},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 400

    request, response = test_client.post(
        "/api/products",
        json={"name": "Pencil", "description": "Awesome pensil", "price": 0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 400


@pytest.mark.parametrize(
    "test_input, expected", [("admin_token", 200), ("user_token", 200)]
)
def test_get_all_product(test_client: Sanic, data: dict, test_input, expected):
    token = data[test_input]
    request, response = test_client.get(
        "/api/products",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == expected
    assert response.json["products"][0]["product_id"] == data["product_id"]
    assert response.json["products"][0]["name"] == "Pencil"
    assert response.json["products"][0]["description"] == "Awesome pensil"
    assert response.json["products"][0]["price"] == 44.44


@pytest.mark.parametrize(
    "test_input, expected", [("admin_token", 200), ("user_token", 200)]
)
def test_get_product(test_client: Sanic, data: dict, test_input, expected):
    token = data[test_input]
    product_id = data["product_id"]
    request, response = test_client.get(
        f"/api/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == expected
    assert response.json["product_id"] == data["product_id"]
    assert response.json["name"] == "Pencil"
    assert response.json["description"] == "Awesome pensil"
    assert response.json["price"] == 44.44


@pytest.mark.parametrize(
    "test_input, expected", [("admin_token", 200), ("user_token", 403)]
)
def test_update_product(test_client: Sanic, data: dict, test_input, expected):
    token = data[test_input]
    product_id = data["product_id"]
    request, response = test_client.put(
        f"/api/products/{product_id}",
        json={"name": "Apple", "description": "Awesome apple", "price": 11.11},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == expected

    product_id = data["product_id"]
    request, response = test_client.get(
        f"/api/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.json["product_id"] == data["product_id"]
    assert response.json["name"] == "Apple"
    assert response.json["description"] == "Awesome apple"
    assert response.json["price"] == 11.11


def test_update_product_invalid_data(test_client: Sanic, data: dict):
    token = data["admin_token"]
    product_id = data["product_id"]
    request, response = test_client.put(
        f"/api/products/{product_id}",
        json={"name": "", "description": "Awesome pensil", "price": 44.44},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 400

    request, response = test_client.put(
        f"/api/products/{product_id}",
        json={"name": "Pencil", "description": "", "price": 44.44},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 400

    request, response = test_client.put(
        f"/api/products/{product_id}",
        json={"name": "Pencil", "description": "Awesome pensil", "price": 0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 400

    request, response = test_client.put(
        f"/api/products/{product_id}",
        json={"name": "Pencil", "description": "Awesome pensil", "price": 12.222},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 400


@pytest.mark.parametrize(
    "test_input, expected", [("admin_token", 200), ("user_token", 403)]
)
def test_patch_product(test_client: Sanic, data: dict, test_input, expected):
    token = data[test_input]
    product_id = data["product_id"]
    request, response = test_client.patch(
        f"/api/products/{product_id}",
        json={"name": "Car"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == expected

    product_id = data["product_id"]
    request, response = test_client.get(
        f"/api/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.json["product_id"] == data["product_id"]
    assert response.json["name"] == "Car"
    assert response.json["description"] == "Awesome apple"
    assert response.json["price"] == 11.11


def test_patch_product_other_fields(test_client: Sanic, data: dict):
    product_id = data["product_id"]
    token = data["admin_token"]
    request, response = test_client.patch(
        f"/api/products/{product_id}",
        json={"description": "Awesome car"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 200

    product_id = data["product_id"]
    request, response = test_client.get(
        f"/api/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.json["product_id"] == data["product_id"]
    assert response.json["name"] == "Car"
    assert response.json["description"] == "Awesome car"
    assert response.json["price"] == 11.11

    request, response = test_client.patch(
        f"/api/products/{product_id}",
        json={"price": 1311.94},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 200

    product_id = data["product_id"]
    request, response = test_client.get(
        f"/api/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.json["product_id"] == data["product_id"]
    assert response.json["name"] == "Car"
    assert response.json["description"] == "Awesome car"
    assert response.json["price"] == 1311.94


def test_putch_product_invalid_data(test_client: Sanic, data: dict):
    token = data["admin_token"]
    product_id = data["product_id"]
    request, response = test_client.patch(
        f"/api/products/{product_id}",
        json={"name": ""},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 400

    request, response = test_client.patch(
        f"/api/products/{product_id}",
        json={"description": ""},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 400

    request, response = test_client.patch(
        f"/api/products/{product_id}",
        json={"price": 0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 400

    request, response = test_client.patch(
        f"/api/products/{product_id}",
        json={"price": 123.123},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 400


def test_admin_delete_product(test_client: Sanic, data: dict):
    token = data["admin_token"]
    request, response = test_client.post(
        "/api/products",
        json={"name": "Phone", "description": "Awesome phone", "price": 156.44},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 201
    product_id = response.json["product_id"]

    request, response = test_client.delete(
        f"/api/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 204

    request, response = test_client.get(
        f"/api/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 404


def test_user_delete_product(test_client: Sanic, data: dict):
    token = data["user_token"]
    product_id = data["product_id"]

    request, response = test_client.delete(
        f"/api/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 403

    request, response = test_client.get(
        f"/api/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 200
