from fastapi import (APIRouter, Body, HTTPException, Request, Depends)
from bson import ObjectId
from api.controller import order_controller, auth_controller, cart_controller
from api.models.order import Order
from api.models.user import User

router_order = APIRouter(prefix="/api/v1/orders", tags=["orders"])

@router_order.get("/")
async def get_order(current_user: User = Depends(auth_controller.get_current_user)):
    orders = await cart_controller.get_carts(current_user)
    for order in orders:
        id = str(order["_id"])
        order["_id"] = id
    return{
        "status":"success",
        "result": len(orders),
        "data": {
            "listCart":orders, 
            'email': current_user['email'],
            'name': current_user['name']
            }
    }

@router_order.post("/")
async def post_order(request: Request, current_user: User = Depends(auth_controller.get_current_user)):
    data = await request.json()
    carts = await cart_controller.get_carts(current_user)
    order = await order_controller.post_order(carts,data,current_user)
    if not order:
        raise HTTPException(404,"Could not find product")
    else:
        return{
            "status": "success",
            "order_id": order
        }
    
@router_order.get("/getBill")
async def get_bill(id:str, current_user: User = Depends(auth_controller.get_current_user)):
    bill = await order_controller.get_bill(id)
    if not bill:
        raise HTTPException(404,"Could not find product")
    else:
        return bill
    
@router_order.get("/purchase-history")
async def get_my_order(status:int, current_user: User = Depends(auth_controller.get_current_user)):
    orders = await order_controller.get_my_order(status,current_user)
    if not orders or orders == None:
        orders=""
    else:
        return{
            "status":"success",
            "data": {
                "order":orders, 
                }
        }
    
@router_order.get("/purchase-history/totalOrder")
async def total_order(current_user: User = Depends(auth_controller.get_current_user)):
    orders = await order_controller.total_order(current_user)
    return orders

@router_order.post("/purchase-history")
async def cancelled_my_order(id:str,status:int,current_user: User = Depends(auth_controller.get_current_user)):
    orders = await order_controller.cancelled_my_order(id,status,current_user)
    if not orders or orders == None:
        orders=""
    else:
        return{
            "status":"success",
            "data": {
                "order":orders, 
                }
        }