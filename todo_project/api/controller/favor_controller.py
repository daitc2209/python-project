from api.models.favor import Favor
from api.models.user import User
from bson import ObjectId
from api.config.db import (myFavor, myProduct)

async def get_favors(user: User ):
    favors = myFavor.find({'user_id': str(user['_id'])})
    list_favor = []
    for favor in favors:
        product = myProduct.find_one({'_id': ObjectId(str(favor['product_id']))})
        if product:
            favor['name'] = product['name']
            favor['price'] = product['price']
            favor['img'] = product['img']
            favor['description'] = product['description']
            favor['discount'] = product['discount']
            list_favor.append(favor)
    
    return list_favor

async def add_to_favors(user: User, product_id: str):
    favor = myFavor.find_one({"user_id": str(user['_id']), "product_id": product_id})
    if favor:
        return {'responseCode': 2}
    else:
        new_favor = Favor(user_id=str(user['_id']), product_id=product_id)
        inserted_id = myFavor.insert_one(dict(new_favor)).inserted_id
        favor = myFavor.find_one({"_id": inserted_id})
        return {'responseCode': 1}


async def delete_favor(id:str):
    favor = myFavor.find_one({'_id': ObjectId(id)})
    if favor:
        myFavor.delete_one(favor)
    return favor

