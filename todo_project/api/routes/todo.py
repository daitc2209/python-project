from fastapi import (APIRouter, HTTPException, Body, Depends,status, Request)
from api.models.user import User
from api.schemas.todo import todos_serializer
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from api.controller import (
    auth_controller,
    user_controller
    )
from api.models.security import (
    Token
)

router = APIRouter(prefix="/api/v1", tags=["users"])

@router.post("/users/signup")
async def sign_up(user: User = Body(default=None)):
    is_exist_user = await auth_controller.is_exist_user(user)
    if is_exist_user:
        create_user:User = await auth_controller.sign_up(user)
        response = await user_controller.user_key(create_user)
        return {"status": "success","data": response}
    else:
        raise HTTPException(404,f"email or user already exist")
    
@router.post("/users/token",response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_controller.auth_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate":"Bearer "}
        )
    access_token = await auth_controller.create_access_token(user['username'],timedelta(minutes=60))

    return {'access_token':access_token, "refresh_token":access_token ,'name': user['name'],'role': user['role']}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(auth_controller.get_current_user)):
    response = await user_controller.user_key(current_user)
    return response

@router.patch("/users/updateme")
async def update_me(user_patch: dict = Body(...),
                    current_user: User = Depends(auth_controller.get_current_user)):
    user = await user_controller.patch_user(user_patch, current_user)
    id = str(user['_id'])
    user['_id'] = id
    return {"status":"success","data updated for user": user}

@router.post("/users/profile/change-password")
async def change_pw(oldPW:str,newPW:str,
                    current_user: User = Depends(auth_controller.get_current_user)):
    user = await user_controller.change_pw(oldPW,newPW,current_user)
    return user


admin = auth_controller.RoleCheck(["admin"])

@router.get("/admin/get_users",dependencies=[Depends(admin)])
async def get_users(request: Request, page: int | None = 1, limit: int | None = 100):
    query = request.query_params._dict
    users = await user_controller.get_users(query)
    for user in users:
        id = str(user["_id"])
        user["_id"] = id
    return{
        "status":"success",
        "result": len(users),
        "data": users
    }

@router.get("/admin/card",dependencies=[Depends(admin)])
async def get_card():
    card = await user_controller.get_card()
    return card

@router.post("/admin/create_user",dependencies=[Depends(admin)])
async def post_user(user:User):
    user = await user_controller.post_user(user)
    id = str(user['_id'])
    user['_id'] = id
    return {
        "status": "success",
        "data": {
            "user": user,
        },
    }

@router.get("/admin/{id:str}")
async def read_user(id:str):
    response = await user_controller.read_user(id)
    return response

@router.patch("/admin/update",dependencies=[Depends(admin)])
async def admin_patch(user_patch: dict = Body(...)):
    user = await user_controller.patch_user_admin(user_patch)
    id = str(user['_id'])
    user['_id'] = id
    return {"status":"success","data updated for user": user}

@router.delete("/admin/delete/{id:str}",dependencies=[Depends(admin)])
async def delete_user(id:str, current_user: User = Depends(auth_controller.get_current_user)):
    user = await user_controller.delete(id,current_user)
    id = str(user['_id'])
    user['_id'] = id
    if not user:
        raise HTTPException(404, "could not find item")
    return {
        "status": "success",
        "user deleted": user,
    }