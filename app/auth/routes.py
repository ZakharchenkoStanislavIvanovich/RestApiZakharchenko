from fastapi import APIRouter, HTTPException, Depends, status
from app.auth.models import UserCreate, UserDB, Token, RefreshTokenRequest
from app.auth.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    users_collection
)
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(tags=["Auth"])

@auth_router.post("/register", response_model=UserDB)
async def register(user: UserCreate):
    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_dict = {
        "email": user.email,
        "password": hash_password(user.password)
    }
    result = await users_collection.insert_one(user_dict)
    return UserDB(id=str(result.inserted_id), **user.dict())

@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access = create_access_token(str(user["_id"]))
    refresh = create_refresh_token(str(user["_id"]))
    return Token(access_token=access, refresh_token=refresh)

@auth_router.post("/refresh", response_model=Token)
async def refresh_token(data: RefreshTokenRequest):
    refresh_token = data.refresh_token
    from jose import JWTError, jwt
    try:
        payload = jwt.decode(refresh_token, "your-secret-key", algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        access = create_access_token(user_id)
        new_refresh = create_refresh_token(user_id)
        return Token(access_token=access, refresh_token=new_refresh)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
