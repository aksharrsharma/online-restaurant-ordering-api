from . import orders, order_details
from . import orders, order_details, payments, promos, recipes, resources, reviews, sandwiches, users


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(payments.router)
    app.include_router(promos.router)
    app.include_router(recipes.router)
    app.include_router(resources.router)
    app.include_router(reviews.router)
    app.include_router(sandwiches.router)
    app.include_router(users.router)