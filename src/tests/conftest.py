import pytest
from sanic import Sanic
from sanic_jwt import Initialize
from sanic_testing.reusable import ReusableClient
from tortoise.contrib.sanic import register_tortoise

from blueprints import api
from blueprints.auth.views import (add_scopes_to_payload, authenticate,
                                   retrieve_user)
from common.utilities import create_access_token


@pytest.fixture(scope="session")
def test_client():
    app = Sanic("TestApp")
    app.blueprint(api)

    register_tortoise(
        app,
        db_url="sqlite://:memory:",
        modules={
            "models": [
                "blueprints.products.models",
                "blueprints.users.models",
                "blueprints.bills.models",
                "blueprints.transactions.models",
            ]
        },
        generate_schemas=True,
    )

    Initialize(
        app,
        authenticate=authenticate,
        retrieve_user=retrieve_user,
        add_scopes_to_payload=add_scopes_to_payload,
        url_prefix="/api",
        path_to_authenticate="/signin",
        path_to_retrieve_user="/me",
    )

    client = ReusableClient(app)
    client.run()
    yield client
    client.stop()


@pytest.fixture(scope="session")
def data():
    return {}
