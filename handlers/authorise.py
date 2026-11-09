from datetime import UTC, datetime, timedelta
from typing import Annotated, cast

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.main import get_session
from .router import router
from .schemes import Token
from db.models import User

SECRET_KEY = "cb32e9ded39339be7b9d739e58464af275470a13907d45673cf780caee2d68d0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_session)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учётные данные",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except (InvalidTokenError, KeyError, TypeError, ValueError):
        raise credentials_exception

    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise credentials_exception

    return user


async def get_current_admin(
    current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав. Требуются права администратора.",
        )

    return current_user

async def get_current_role(current_user: Annotated[User, Depends(get_current_user)]):
    role = cast(str, current_user.role)
    if role == "Admin":
        return current_user

    elif role == "Teacher":
        return current_user

    elif role == "Student":
        return current_user

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав")



@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    result = await db.execute(
        select(User).where(User.username == form_data.username)
    )
    user = result.scalar_one_or_none()

    if user is None or not password_hash.verify(
        form_data.password,
        user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь неактивен",
        )

    access_token = create_access_token(
        data={"sub": str(user.id),
              "role": user.role}
    )
    print(access_token)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


