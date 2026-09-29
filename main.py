from fastapi import FastAPI
from routers import categories, orders, users, products,payments, order_items

app = FastAPI()

app.include_router(categories.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(order_items.router)
app.include_router(payments.router)




