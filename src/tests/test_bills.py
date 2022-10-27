import pytest
from sanic import Sanic


@pytest.mark.parametrize(
    "test_input, expected",
    [("user_token", 201), ("anonymous_user_token", 401)],
)
def test_add_bill(test_client: Sanic, data: dict, test_input, expected):
    data["anonymous_user_token"] = "invalid_token"
    token = data[test_input]
    request, response = test_client.post(
        "/api/bills",
        headers={"Authorization": f"Bearer {token}"},
    )
    if test_input == "user_token":
        data["bill_id"] = response.json["bill_id"]
    assert response.status == expected


def test_get_bill(test_client: Sanic, data: dict):
    token = data["user_token"]
    request, response = test_client.get(
        f"/api/bills/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status == 200
    assert response.json["bills"][0]["bill_id"] == data["bill_id"]
    assert response.json["bills"][0]["balance"] == 0
