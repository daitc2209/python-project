
from fastapi import (APIRouter, Body, HTTPException, Request, Security, Depends)
from bson import ObjectId
from api.controller import favor_controller, auth_controller
from api.models.favor import Favor
from api.models.user import User

router_favor = APIRouter(prefix="/api/v1/favors", tags=["favors"])

user = auth_controller.RoleCheck(["admin", "user"])

@router_favor.get("/")
async def get_all_favor(current_user: User = Depends(auth_controller.get_current_user)):
    favors = await favor_controller.get_favors(current_user)
    for favor in favors:
        id = str(favor["_id"])
        favor["_id"] = id
    return{
        "status":"success",
        "result": len(favors),
        "data": favors
    }

@router_favor.post("/add-to-favor")
async def add_to_favor(product_id:str, current_user: User = Depends(auth_controller.get_current_user)):
    favor = await favor_controller.add_to_favors(current_user,product_id)
    if not favor :
        raise HTTPException(404,"Could not find item")
    if favor:
        return favor
    
@router_favor.get("/delete-favor", dependencies= [Depends(user)])
async def delete_favor(id:str):
    print(f"{id}")
    favor = await favor_controller.delete_favor(id)
    id = str(favor['_id'])
    favor['_id'] = id
    if not favor:
        raise HTTPException(404, "could not find item")
    return {
        "status": "success",
        "favor deleted": favor,
    }
