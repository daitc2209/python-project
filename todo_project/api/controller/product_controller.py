from api.models.product import Product
from datetime import datetime
from fastapi import HTTPException
from bson import ObjectId
from api.config.db import myProduct as db
from pymongo import DESCENDING
from api.controller import auth_controller
import re

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

async def get_products(query: dict):
    sort_by, skip, limit = query_params(query)
    search_text = query.get("search_text")
    if search_text:
        regex = re.compile(f".*{re.escape(search_text)}.*", re.IGNORECASE)
        products = db.find({
            "$or": [
                {"name": {"$regex": regex}},
                {"brand": {"$regex": regex}},
                {"category": {"$regex": regex}}
            ]
        }).sort(sort_by).skip(skip).limit(limit)
    else:
        products = db.find().sort(sort_by).skip(skip).limit(limit)
    return list(products)

async def get_product(Id):
    product = db.find_one({"_id": ObjectId(Id)})
    return product

async def post(product):
    discount = int(product['discount'])  
    if discount > 100:
        product['discount'] = 100
    if discount < 0:
        product['discount'] = 0
    inserted_id = db.insert_one(dict(product)).inserted_id
    return {"_id":inserted_id}

def validate_patch_body(patch:dict, model):
    keys = patch.keys()
    return all(k in model for k in keys)

async def patch_product(Id, new_product:dict):
    product = db.find_one({"_id": ObjectId(Id)})
    if product:
        if validate_patch_body(new_product, product):
            discount = int(new_product['discount'])  
            if discount > 100:
                new_product['discount'] = 100
            if discount < 0:
                new_product['discount'] = 0
            for k, v in new_product.items():
                if k != "_id":
                    product[k] = v
            db.update_one({"_id": ObjectId(Id)}, {"$set": product})
    return product

async def delete_product(Id):
    product = db.find_one({'_id': ObjectId(Id)})
    if product:
        db.delete_one(product)
    return product
