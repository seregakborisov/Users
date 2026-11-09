from typing import Annotated

from .authorise import get_current_admin, get_current_user, password_hash
from fastapi import Depends, HTTPException, status
from .schemes import AddUserSchema, UserAdminSchema, UserSchema, UserSelfSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.main import get_session
from db.models import User
from .router import router


@router.post("/registration")
async def registration(
    user: UserSchema, db: Annotated[AsyncSession, Depends(get_session)]
):
    new_user = User(
        username=user.username,
        password=password_hash.hash(user.password),
        role="Student",
    )

    db.add(new_user)
    await db.commit()

    return {"username": "Вы зарегистрированы!"}


@router.get("/self", response_model=UserSelfSchema)
async def get_self(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/users", response_model=list[UserSelfSchema])
async def get_users(
    db: Annotated[AsyncSession, Depends(get_session)],
    admin: Annotated[User, Depends(get_current_admin)],
):
    result = await db.execute(select(User))
    return result.scalars().all()


@router.post("/user_add")
async def user_add(
    user: AddUserSchema,
    db: Annotated[AsyncSession, Depends(get_session)],
    admin: Annotated[User, Depends(get_current_admin)],
):
    new_user = User(
        username=user.username,
        is_active=user.is_active,
        is_admin=user.is_admin,
        balance=user.balance,
        password=password_hash.hash(user.password),
    )

    db.add(new_user)
    await db.commit()

    return {"username": "Пользователь добавлен!"}


@router.put("/up_self")
async def update_self(
    user_data: UserSchema,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    if user_data.username is not None:
        current_user.username = user_data.username

    if user_data.password is not None:
        current_user.password = password_hash.hash(user_data.password)

    await db.commit()

    return {"message": "Данные пользователя обновлены"}


@router.put("/uppdate_admin")
async def update_user_admin(
    user_id: int,
    user_data: UserAdminSchema,
    db: Annotated[AsyncSession, Depends(get_session)],
    admin: Annotated[User, Depends(get_current_admin)],
):
    user = await db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )

    if user_data.username is not None:
        user.username = user_data.username

    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    if user_data.is_admin is not None:
        user.is_admin = user_data.is_admin

    if user_data.balance is not None:
        user.balance = user_data.balance

    await db.commit()

    return {"message": "Данные пользователя обновлены"}


@router.delete("/deactivate")
async def deactivate_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_session)],
    admin: Annotated[User, Depends(get_current_admin)],
):
    user = await db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь уже неактивен"
        )

    user.is_active = False
    await db.commit()

    return {"message": "Пользователь деактивирован"}
