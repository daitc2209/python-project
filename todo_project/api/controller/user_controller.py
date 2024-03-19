from api.models.user import User
from api.config.db import myUser as db
from api.config.db import myOrder
from api.config.db import myProduct
from bson import ObjectId
from fastapi import HTTPException
from api.controller import auth_controller
from pymongo import DESCENDING
import re

authentication_fields = [
    "username",
    "role" "password",
]

authentication_fields_admin = [
    "username","password"
]

async def user_key(user:User, keys: list=["username","name","email","role","address"]):
    return_user = {}
    return_user["_id"] = f"{user['_id']}"
    for k,v in user.items():
        if k in keys:
            return_user[k] = v
    return return_user 

def validate_patch_body(patch, model, role):
    keys = patch.keys()
    if role == "user":
        if any(k in authentication_fields for k in keys):
            raise HTTPException(400, "cannot update authentication field")
    if role == "admin":
        if any(k in authentication_fields_admin for k in keys):
            raise HTTPException(400, "cannot update authentication field")
    return all(k in model for k in keys)

async def patch_user(user_patch: dict, current_user: User):
    user = current_user
    check_email = db.find_one({"email":user_patch.get("email")})
    if check_email and check_email['email'] != user['email']:
        raise HTTPException(400, "exist email !!")
    if validate_patch_body(user_patch,user,"user"):
        for k, v in user_patch.items():
            if k != "_id":
                user[k] = v
            db.update_one({"_id": ObjectId(user['_id'])}, {"$set": user})
    return user

async def change_pw(old_pw,new_pw, current_user: User):
    if auth_controller.verify_pw(old_pw,current_user['password']):
        current_user['password'] = auth_controller.get_pw_hash(new_pw)
        db.update_one({"_id": ObjectId(current_user['_id'])}, {"$set": current_user})
        return {"status": 1, "message": "change password success !!"}
    else:
        return {"status": 0, "message": "change password failed !!"}
        
async def get_users(query:dict):
    sort_by, skip, limit = query_params(query)
    search_text = query.get("search_text")
    if search_text:
        regex = re.compile(f".*{re.escape(search_text)}.*", re.IGNORECASE)
        users = db.find({
            "$or": [
                {"name": {"$regex": regex}},
                {"email": {"$regex": regex}},
                {"username": {"$regex": regex}},
                {"role": {"$regex": regex}},
                {"address": {"$regex": regex}}
            ]
        }).sort(sort_by).skip(skip).limit(limit)
    else:
        users = db.find().sort(sort_by).skip(skip).limit(limit)
    return list(users)

def query_params(query: dict):
    sort_by = query.get("sort")
    if sort_by:
        sort_by = [(field.strip(), DESCENDING) for field in sort_by.split(",")]
    else:
        sort_by = [("createdAt", DESCENDING)]
    limit = int(query.get("limit")) if  query.get("limit") else 100
    page = int(query.get("page")) if  query.get("page") else None
    skip = (page - 1) if page else 0
    return sort_by, skip, limit

# Admin
async def get_card():
    users = db.find({"role":"user"})
    orders_pending = myOrder.find({"state_order":0})
    orders = myOrder.find()
    products = myProduct.find()
    return {
        "users": len(list(users)),
        "orders": len(list(orders)),
        "orders_pending": len(list(orders_pending)),
        "products": len(list(products))
    }

async def post_user(user:User):
    check_email = db.find_one({"email":user.email})
    check_username = db.find_one({"username":user.username})
    if check_email or check_username:
        raise HTTPException(401, "exist email or username !!")
    inserted_id = db.insert_one(dict(user)).inserted_id
    return {"_id":inserted_id}

async def read_user(id:str, keys: list=["username","name","email","role","address"]):
    return_user = {}
    user = db.find_one({"_id":ObjectId(id)})
    return_user["_id"] = f"{user['_id']}"
    for k,v in user.items():
        if k in keys:
            return_user[k] = v
    return return_user 

async def patch_user_admin(user_patch: dict):
    user = db.find_one({'_id':ObjectId(user_patch['_id'])})
    
    if user:
        check_email = db.find_one({"email":user_patch.get("email")})
        if check_email and check_email['email'] != user['email']:
            raise HTTPException(401, "exist email !!")
        if validate_patch_body(user_patch,user,"admin"):
            for k, v in user_patch.items():
                if k != "_id":
                    user[k] = v
                db.update_one({"_id": ObjectId(user['_id'])}, {"$set": user})
    return user

async def delete(Id,current_user:User):
    user = db.find_one({'_id': ObjectId(Id)})
    if user['username'] == current_user['username']:
        raise HTTPException(400, "Không thể xóa tài khoản đang sử dụng")
    if user:
        db.delete_one(user)
    return user