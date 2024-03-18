from api.models.cart import Cart
from api.models.user import User
from bson import ObjectId
from api.config.db import (myCart, myProduct)

async def get_carts(user: User ):
    carts = myCart.find({'user_id': str(user['_id'])})
    list_cart = []
    for cart in carts:
        product = myProduct.find_one({'_id': ObjectId(str(cart['product_id']))})
        if product:
            cart['name'] = product['name']
            cart['price'] = product['price']
            cart['img'] = product['img']
            cart['discount'] = product['discount']
            cart['quantity_in_stock'] = product['quantity']
            cart['totalPrice'] = cart['price']*cart['amount'] - (cart['price']*cart['amount']*cart['discount']/100)
            list_cart.append(cart)
    
    return list_cart

async def add_to_carts(user: User, product_id: str, num: int):
    cart = myCart.find_one({"user_id": str(user['_id']), "product_id": product_id})
    if cart:
        cart['amount'] += num
        myCart.update_one({"_id": cart['_id']}, {"$set": cart})
    else:
        new_cart = Cart(user_id=str(user['_id']), product_id=product_id, amount=num)
        inserted_id = myCart.insert_one(dict(new_cart)).inserted_id
        cart = myCart.find_one({"_id": inserted_id})
    return cart

    

async def edit_cart(id:str, num:int):
    cart = myCart.find_one({"_id": ObjectId(id)})
    cart['amount'] += num
    myCart.update_one({"_id": ObjectId(id)}, {"$set": cart})
    return cart

async def delete_cart(id:str):
    cart = myCart.find_one({'_id': ObjectId(id)})
    if cart:
        myCart.delete_one(cart)
    return cart

async def clear_cart(user: User):
    myCart.delete_many({"user_id": str(user['_id'])})
    return {
        "status": "success",
        "cart clear": "clear success"
    }

