from api.models.user import User
from api.config.db import myUser as db
from bson import ObjectId
from fastapi import HTTPException
from api.controller import auth_controller
from pymongo import DESCENDING

authentication_fields = [
    "username",
    "role" "password",
]

def user_key(user:User, keys: list=["username","name","email","role","address"]):
    return_user = {}
    return_user["_id"] = f"{user['_id']}"
    for k,v in user.items():
        if k in keys:
            return_user[k] = v
    return return_user 

def validate_patch_body(patch, model):
    keys = patch.keys()
    if any(k in authentication_fields for k in keys):
        raise HTTPException(401, "cannot update authentication field")
    return all(k in model for k in keys)

async def patch_user(user_patch: dict, current_user: User):
    user = current_user
    if validate_patch_body(user_patch,user):
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