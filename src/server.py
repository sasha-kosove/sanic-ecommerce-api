from sanic import Sanic
from sanic_jwt import Initialize
from tortoise.contrib.sanic import register_tortoise

from blueprints import api
from blueprints.auth.views import (add_scopes_to_payload, authenticate,
                                   retrieve_user)
from config import (POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD,
                    POSTGRES_USER, app_config)

app = Sanic(__name__)
app.blueprint(api)
app.config.update(app_config)

register_tortoise(
    app,
    db_url=f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}",
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, fast=True, dev=True)
