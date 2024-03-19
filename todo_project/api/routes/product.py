
from fastapi import (APIRouter, Body, HTTPException, Request, Security, Depends)
from bson import ObjectId
from api.controller import product_controller, auth_controller
from api.models.product import Product

router_product = APIRouter(prefix="/api/v1/products", tags=["products"])

@router_product.get("/")
async def get_all_product(request: Request, page: int | None = 1, limit: int | None = 100):
    query = request.query_params._dict
    products = await product_controller.get_products(query)
    for product in products:
        id = str(product["_id"])
        product["_id"] = id
    return{
        "status":"success",
        "result": len(products),
        "data": products
    }

@router_product.get("/{Id}")
async def get_product(Id: str):
    product = await product_controller.get_product(Id)
    id = str(product["_id"])
    product["_id"] = id
    if not product:
        raise HTTPException(404,"Could not find product")
    else:
        return{
            "status": "success",
            "data": product
        }
    
admin = auth_controller.RoleCheck(["admin"])

@router_product.post("/create", dependencies=[Depends(admin)])
async def create_product(product: Product):
    product = await product_controller.post(product)
    id = str(product['_id'])
    product['_id'] = id
    return {
        "status": "success",
        "data": {
            "product": product,
        },
    }

@router_product.patch("/{Id:str}",dependencies=[Depends(admin)])
async def update_product(Id: str, product_patch:dict = Body(...)):
    product = await product_controller.patch_product(Id, product_patch)
    id = str(product['_id'])
    product['_id'] = id
    if not product :
        raise HTTPException(404,"Could not find item")
    if product:
        return {
            "status": "success",
            "product updated to": product
        }
    
@router_product.delete("/delete/{Id:str}", dependencies=[Depends(admin)])
async def delete_product(Id: str):
    product = await product_controller.delete_product(Id)
    id = str(product['_id'])
    product['_id'] = id
    if not product:
        raise HTTPException(404, "could not find item")
    return {
        "status": "success",
        "product deleted": product,
    }
