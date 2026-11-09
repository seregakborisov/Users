from typing import Annotated

import aiohttp
from .authorise import get_current_user
from fastapi import Depends

from .router import router
from db.models import User


async def create_lesson(user_id: int, lesson_name: str):
    url = "http://127.0.0.1:8001/user_visit"

    async with (
        aiohttp.ClientSession() as session,
        session.post(
            url,
            json={
                "user_id": user_id,
                "lesson_name": lesson_name,
            },
        ) as response,
    ):
        return await response.json()


@router.get("/visit/{lesson_name}")
async def visit_lesson(
    lesson_name: str,
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await create_lesson(current_user.id, lesson_name)
