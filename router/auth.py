from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import User
from libs.db import session
from pydantic import BaseModel
from libs.password import hash_password, verify_password
from libs.token import create_access_token, decode_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class RegisterInput(BaseModel):
    name: str
    email: str
    password: str

class LoginInput(BaseModel):
    email: str
    password: str

async def get_user(email: str):
    user = session.query(User).filter(User.email==email).first()
    return user

@router.post("/login")
async def login(body: LoginInput):
    user = await get_user(body.email)

    if not user:
        return {
            "success": False,
            "message": "Email not found"
        }
    
    verify = await verify_password(body.password, user.password)

    if not verify:
        return {
            "success": False,
            "message": "Email and password combination not match"
        }

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "success": True,
        "access_token": access_token
    }

@router.post("/register")
async def register(body: RegisterInput):
    exists = await get_user(body.email)

    if exists:
        return {
            "success": False,
            "message": "Email already exists"
        }

    hashed_password = await hash_password(body.password)
    user = User(name=body.name, email=body.email, password=hashed_password)
    session.add(user)
    session.commit()

    return {
        "success": True,
        "message": "User created"
    }

@router.get("/profile")
async def protected_route(token: str = Depends(oauth2_scheme)):
    email = decode_token(token)
    user = await get_user(email)

    if not user:
        return {
            "success": False,
            "message": "Unauthorized"
        }

    return {
            "success": True,
            "message": None,
            "data": {
                "email": user.email
            }
        }