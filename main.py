from fastapi import FastAPI, Depends, Body, Query, status, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db.main import get_session, init_models
from db.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Annotated, cast
from sqlalchemy import select, update, delete
import asyncio
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
import time

app = FastAPI()

SECRET_KEY = "cb32e9ded39339be7b9d739e58464af275470a13907d45673cf780caee2d68d0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.on_event("startup")
async def startup():
    await init_models()


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class UserSchema(BaseModel):
    username: str
    password: str

class AddUserSchema(BaseModel):
    username: str
    is_active: bool
    is_admin: bool
    balance: float
    password: str 

class UserAdminSchema(BaseModel):
    username: str
    is_active: bool
    is_admin: bool
    balance: float
    #password: str Надо админу право устанавливать пароль пользователя?

class UserSelfSchema(BaseModel):
    id: int
    username: str
    is_active: bool
    is_admin: bool
    balance: float



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db_conn: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except (InvalidTokenError, KeyError, TypeError, ValueError):
        raise credentials_exception
        
    result = await db_conn.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if user is None:
         raise credentials_exception

    if user.is_active is False:
         raise credentials_exception
    
    return user

async def get_current_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not cast(bool, current_user.is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав. Требуются права администратора.",
        )

    return current_user

@app.get("/self", response_model=UserSelfSchema)
async def get_self(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
  

@app.post("/registration")
async def registration(
    user_data: Annotated[UserSchema, Body()],
    db_conn: AsyncSession = Depends(get_session),
):

    hashed_password = password_hash.hash(user_data.password)

    new_user = User(username=user_data.username, password=hashed_password)
    db_conn.add(new_user)

    await db_conn.commit()

    return {user_data.username: "Вы зарегистрированы!"}


@app.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_conn: AsyncSession = Depends(get_session),
):
    result = await db_conn.execute(
        select(User).where(User.username == form_data.username)
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not password_hash.verify(form_data.password, cast(str, user.password)):
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверное имя пользователя или пароль",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if user.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь неактивен",
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    
    return {
    "access_token": access_token,
    "token_type": "bearer",
}
@app.get("/users", response_model=list[UserSelfSchema])
async def get_users(
    admin: Annotated[User, Depends(get_current_admin)],
    db_conn: Annotated[AsyncSession, Depends(get_session)],
):
    result = await db_conn.execute(select(User))
    users = result.scalars().all()

    return users

@app.post("/user_add")
async def user_add(
    user_data: Annotated[AddUserSchema, Body()],
    db_conn: AsyncSession = Depends(get_session),
):
    hashed_password = password_hash.hash(user_data.password)
    new_user = User(
        username=user_data.username,
        is_active=user_data.is_active,
        is_admin=user_data.is_admin,
        balance=user_data.balance,
        password=hashed_password,
    )
    db_conn.add(new_user)

    await db_conn.commit()

    return {"Message": "Пользователь успешно добавлен"}

@app.put("/up_self")
async def up_self(
    user_data: Annotated[UserSchema, Body()],
    current_user: Annotated[User, Depends(get_current_user)],
    db_conn: Annotated[AsyncSession, Depends(get_session)],
):
    current_user.username = user_data.username
    current_user.password = password_hash.hash(user_data.password)

    await db_conn.commit()

    return {
        "message": "Данные пользователя обновлены",
        "user_id": current_user.id,
        "username": current_user.username,
    }

@app.put("/uppdate_admin")
async def update_admin(
    user_id: Annotated[int, Query()],
    user_data: Annotated[UserAdminSchema, Body()],
    admin: Annotated[User, Depends(get_current_admin)],
    db_conn: Annotated[AsyncSession, Depends(get_session)],
):
    result = await db_conn.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    user.username = user_data.username
    user.is_active = user_data.is_active
    user.is_admin = user_data.is_admin
    user.balance = user_data.balance
    #user.password = password_hash.hash(user_data.password)

    await db_conn.commit()
 
    return {
        "message": "Данные пользователя обновлены",
        "user_id": user.id,
        "username": user.username,
    }

@app.delete("/diactivate")
async def deactivate(
    user_id: Annotated[int, Query()],
    admin: Annotated[User, Depends(get_current_admin)],
    db_conn: Annotated[AsyncSession, Depends(get_session)],
):
    result = await db_conn.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    if not cast(bool, user.is_active):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже деактивирован",
        )

    user.is_active = False

    await db_conn.commit()

    return {
        "message": "Пользователь деактивирован",
        "user_id": user.id,
        "username": user.username,
        "is_active": user.is_active,
    }
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response




