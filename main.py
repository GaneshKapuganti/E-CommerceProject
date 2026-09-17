from fastapi import FastAPI
from routers import categories, orders, users, products,payments, order_items
from database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(categories.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(order_items.router)
app.include_router(payments.router)




