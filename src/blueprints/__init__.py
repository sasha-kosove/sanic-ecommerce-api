from sanic import Blueprint

from .auth.views import bp as auth_bp
from .bills.views import bp as bills_bp
from .payments.views import bp as payment_bp
from .products.views import bp as products_bp
from .transactions.views import bp as transactions_bp
from .users.views import bp as users_bp

api = Blueprint.group(
    users_bp,
    products_bp,
    auth_bp,
    bills_bp,
    transactions_bp,
    payment_bp,
    url_prefix="/api",
)
