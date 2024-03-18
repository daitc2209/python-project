
from fastapi import (APIRouter, Body, HTTPException, Request, Security, Depends)
from bson import ObjectId
from api.controller import cart_controller, auth_controller
from api.models.cart import Cart
from api.models.user import User

router_cart = APIRouter(prefix="/api/v1/carts", tags=["carts"])

user = auth_controller.RoleCheck(["admin", "user"])

@router_cart.get("/")
async def get_all_cart(current_user: User = Depends(auth_controller.get_current_user)):
    carts = await cart_controller.get_carts(current_user)
    for cart in carts:
        id = str(cart["_id"])
        cart["_id"] = id
    return{
        "status":"success",
        "result": len(carts),
        "data": carts
    }

@router_cart.post("/add-to-cart")
async def add_to_cart(product_id:str, num:int, current_user: User = Depends(auth_controller.get_current_user)):
    cart = await cart_controller.add_to_carts(current_user,product_id,num)
    id = str(cart['_id'])
    cart['_id'] = id
    if not cart :
        raise HTTPException(404,"Could not find item")
    if cart:
        return {
            "status": "success",
            "cart updated to": cart
        }

@router_cart.get("/edit-cart/{id:str}", dependencies=[Depends(user)])
async def edit_cart(id:str, num: int | None = 0):
    carts = await cart_controller.edit_cart(id,num)
    id = str(carts['_id'])
    carts['_id'] = id
    if not carts :
        raise HTTPException(404,"Could not find item")
    if carts:
        return {
            "status": "success",
            "carts updated to": carts
        }
    
@router_cart.get("/delete-cart/{id:str}", dependencies= [Depends(user)])
async def delete_cart(id:str):
    cart = await cart_controller.delete_cart(id)
    id = str(cart['_id'])
    cart['_id'] = id
    if not cart:
        raise HTTPException(404, "could not find item")
    return {
        "status": "success",
        "cart deleted": cart,
    }

@router_cart.get("/clear-cart")
async def clear_cart(current_user:User = Depends(auth_controller.get_current_user)):
    cart = await cart_controller.clear_cart(current_user)
    return cart