from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.todo import router
from api.routes.product import router_product
from api.routes.cart import router_cart
from api.routes.order import router_order
from api.routes.favor import router_favor

origins = ["*"]
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "*"
]

app = FastAPI()
app.include_router(router)
app.include_router(router_product)
app.include_router(router_cart)
app.include_router(router_order)
app.include_router(router_favor)
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE","PATCH"],
        allow_headers=["*"],
    )
# @app.get("/")
# def index():
#     return {"status": "todo api is running"}
