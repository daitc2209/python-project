from api.models.user import User
from api.models.order import Order
from api.models.order_detail import Order_details
from api.config.db import myOrder, myOrderDetail, myCart, myProduct
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from pymongo import DESCENDING
import re

async def post_order(carts: list, data:dict, user:User):
    amount = sum(n['amount'] for n in carts)
    total = sum(n['totalPrice'] for n in carts) + 40000
    order = Order(
        user_id=str(user['_id']),
        address_delivery=data.get("address"),
        email=user['email'],
        name=user['name'],
        phone=data.get('phone'),
        amount=amount,
        note=data.get('note'),
        total_money=total)
    insert_id = myOrder.insert_one(dict(order)).inserted_id
    for cart in carts:
        product = myProduct.find_one({"_id": ObjectId(cart['product_id'])})
        product['quantity'] = int(product['quantity']) - cart['amount']
        myProduct.update_one({"_id": product['_id']}, {"$set":product})
        orderdetail = Order_details(
            order_id=str(insert_id),product_id=cart['product_id'],amount=cart['amount'],
            discount=cart['discount'],price=cart['price'],total=cart['totalPrice'])
        myOrderDetail.insert_one(dict(orderdetail)).inserted_id

    codeOrder = ""+str(insert_id)+str(user['_id'])
    order = myOrder.find_one({"_id": insert_id})
    order['code_order'] = codeOrder
    myorder =  myOrder.update_one({'_id':insert_id},{"$set": order})
    
    if myorder:
        myCart.delete_many({"user_id": str(user['_id'])})

    return str(insert_id)

async def get_bill(id:str):
    order =  myOrder.find_one({'_id': ObjectId(id)})
    orderDetail = myOrderDetail.find({'order_id': id})
    
    list_od = []
    idd = str(order["_id"])
    order["_id"] = idd
    for od in orderDetail:
        product = myProduct.find_one({'_id': ObjectId(od['product_id'])})
        od['img'] = product['img']
        od['price'] = product['price']
        od['discount'] = product['discount']
        id1 = str(od["_id"])
        od["_id"] = id1
        list_od.append(od)
    return {"order": order, 'orderdetail': list_od}

async def get_my_order(status:int, user: User):
    query = {"user_id": str(user['_id'])}
    if status != 5:
        query["state_order"] = status

    orders = myOrder.find(query)
    order_list = []
    for order in orders:
        orderDetail = await get_bill(str(order['_id']))
        order['orderdetail'] = orderDetail['orderdetail']
        idd = str(order["_id"])
        order["_id"] = idd
        order_list.append(order)
    return order_list

async def total_order(user:User):
    order = myOrder.find({"user_id": str(user['_id'])})
    order_received = myOrder.find({"user_id": str(user['_id']), "state_order": 3})
    return {
        "total_order":len(list(order)),
        "order_received": len(list(order_received)),
        }

async def cancelled_my_order(id:str, status:int, user:User):
    order = myOrder.find_one({"_id": ObjectId(id)})
    order["state_order"] = 4
    order_detals = myOrderDetail.find({"order_id":id})
    for od in order_detals:
        p = myProduct.find_one({"_id": ObjectId(str(od['product_id']))})
        p['quantity'] += od['amount']
        myProduct.update_one({'_id': p['_id']},{'$set':p})
    myOrder.update_one({'_id':order['_id']},{'$set':order})
    list_order = await get_my_order(status,user)
    return list_order


async def get_all_status_order():
    order_received = myOrder.find({ "state_order": 3})
    order_cancelled = myOrder.find({ "state_order": 4})
    order_delivery = myOrder.find({ "state_order": 2})
    order_confirm = myOrder.find({ "state_order": 1})
    order_pending = myOrder.find({ "state_order": 0})
    return {
        "order_received": len(list(order_received)),
        "order_cancelled":len(list(order_cancelled)),
        "order_delivery": len(list(order_delivery)),
        "order_confirm":len(list(order_confirm)),
        "order_pending":len(list(order_pending)),
        }

async def get_all_order(query:dict):
    search_text = query.get("search_text")
    sort_by = [("createdAt", DESCENDING)]
    
    if search_text:
        regex = re.compile(f".*{re.escape(search_text)}.*", re.IGNORECASE)
        orders = myOrder.find({
            "$or": [
                {"name": {"$regex": regex}},
                {"brand": {"$regex": regex}},
                {"category": {"$regex": regex}}
            ]
        }).sort(sort_by)
    else:
        orders = myOrder.find().sort(sort_by)
    order_list = []
    for order in orders:
        orderDetail = await get_bill(str(order['_id']))
        order['orderdetail'] = orderDetail['orderdetail']
        order["_id"] = str(order["_id"])
        order_list.append(order)
    return order_list

async def update_status_order(id:str, status:int):
    order = myOrder.find_one({"_id": ObjectId(id)})
    order["state_order"] = status
    myOrder.update_one({'_id':order['_id']},{'$set':order})
    return {
        "status": "success"
    }