from api.models.user import User
from fastapi import Depends, HTTPException, status
from api.config.db import myUser as db
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl = "/api/v1/users/token"
)

SECRET_KEY = '2948404D6251655468576D5A7134743777217A25432A462D4A614E645266556A'
ALGORITHM = 'HS256'

def get_pw_hash(password):
    return pwd_context.hash(password)

def verify_pw(pw, hash_pw):
    return pwd_context.verify(pw,hash_pw)

async def is_exist_user(user:User):
    user_name = db.find_one({"username" : user.username})
    if user_name:
        raise HTTPException(
            404, f"{user_name['username']} already exist chose another one"
        )
    user_email = db.find_one({"email" : user.email})
    if user_email:
        raise HTTPException(404, f"{user_email['email']} already exist chose another one")
    return user

async def sign_up(user:User):
    check_email = db.find_one({"email":user.email})
    check_username = db.find_one({"username":user.username})
    if check_email or check_username:
        raise HTTPException(401, "exist email or username !!")
    hash_pw = get_pw_hash(user.password)
    user.password = hash_pw
    user = User(
        username=user.username,
        email=user.email,
        password= user.password,
        name=user.name,
        address = user.address,
        createdAt=datetime.now()
    )
    insert_result = db.insert_one(dict(user))
    inserted_user_id = insert_result.inserted_id
    inserted_user = db.find_one({"_id": inserted_user_id})
    return inserted_user

async def auth_user(username:str, password:str):
    user =  db.find_one({"username" : username})
    if not user:
        return False
    if not verify_pw(password, user['password']):
        return False
    return user

async def create_access_token(username: str, expires_delta: timedelta):
    encode = {'sub': username}
    expires = datetime.now() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= ALGORITHM)
        username: str = payload.get('sub')
        user = db.find_one({"username":username})
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
    
class RoleCheck:
    def __init__(self, roles : list):
        self.roles = roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user['role'] not in self.roles:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permission",
                headers={"WWW-Authenticate":"Bearer"}
            )
        

