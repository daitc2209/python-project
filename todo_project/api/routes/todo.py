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

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/signup")
async def sign_up(user: User = Body(default=None)):
    is_exist_user = await auth_controller.is_exist_user(user)
    if is_exist_user:
        create_user:User = await auth_controller.sign_up(user)
        response = user_controller.user_key(create_user)
        return {"status": "success","data": response}
    else:
        raise HTTPException(404,f"email or user already exist")
    
@router.post("/token",response_model=Token)
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


@router.get("/me")
async def read_users_me(current_user: User = Depends(auth_controller.get_current_user)):
    response = user_controller.user_key(current_user)
    return response

@router.patch("/updateme")
async def update_me(user_patch: dict = Body(...),
                    current_user: User = Depends(auth_controller.get_current_user)):
    print(user_patch)
    user = await user_controller.patch_user(user_patch, current_user)
    id = str(user['_id'])
    user['_id'] = id
    return {"status":"success","data updated for user": user}

@router.post("/profile/change-password")
async def change_pw(oldPW:str,newPW:str,
                    current_user: User = Depends(auth_controller.get_current_user)):
    user = await user_controller.change_pw(oldPW,newPW,current_user)
    return user

admin = auth_controller.RoleCheck(["admin"])

@router.get("/",dependencies=[Depends(admin)])
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