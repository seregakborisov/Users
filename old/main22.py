from fastapi import FastAPI, Depends, Header, HTTPException, Request
from pydantic import BaseModel
from typing import Annotated
import time
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
hasher = PasswordHash.recommended()


class User(BaseModel):
    username: str
    is_active: bool
    is_admin: bool
    balance: float


# class Image(BaseModel):
#     url: str
#     name: str


# class Item(BaseModel):
#     name: str
#     age: int
#     photo: Image


# @app.post("/profile")
# async def user_profile(item: Item):
#    return item


# users: list[User] = [ # удалится и вынесется в бд.
#     User(username="Sergey", is_active=True, is_admin=False, balance=15),
#     User(username="Maxim", is_active=True, is_admin=True, balance=1555),
#     User(username="Ivan", is_active=False, is_admin=False, balance=0),
#     User(username="Andrey", is_active=True, is_admin=False, balance=0),]

# @app.post("/user_add")
# async def user_add(
#     user_data: Annotated[MovieSchema, Body()],
#     db_conn: AsyncSession = Depends(get_session),
# ):
#     new_movie = Movie(name=movie_data.name, length=movie_data.length_min)
#     db_conn.add(new_movie)

#     await db_conn.commit()

#     return {"status": "application is running"}


# async def current_user(username: str = Header()):
#     for user in users:
#         if user.username == username:
#             return user
#     raise HTTPException(status_code=401, detail="Пользователь не найден")


# async def active_user(user: User = Depends(current_user)):
#     if user.is_active == True:
#         return user
#     raise HTTPException(status_code=403, detail="No active")


# async def admin_user(user: User = Depends(active_user)):
#     if user.is_admin == True:
#         return user
#     raise HTTPException(status_code=403, detail="No admin")


# async def balance(user: User = Depends(active_user)):
#     if user.balance > 0:
#         return user
#     raise HTTPException(status_code=403, detail="No many")


# @app.get("/testing/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}


# @app.get("/items/public")
# async def user_public(user: Annotated[User, Depends(current_user)]):
#     return {"Welcome,": user.username}


# @app.get("/items/private")
# async def user_active(user: Annotated[User, Depends(active_user)]):
#     return {"Доступен базовый функционал для пользователя": user.username}


# @app.get("/items/pro")
# async def private_user(user: Annotated[User, Depends(balance)]):
#     # TODO: функция называется private_user, но /items/private вверху.
#     return {"Вам доступны платные функции": user.username, "Ваш баланс": user.balance}


# @app.get("/items/admin")
# async def user_admin(user: Annotated[User, Depends(admin_user)]):
#     return {"Добро пожаловать, Админ!": user.username}


# @app.post("/login")
# async def test(formData: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     hashed = hasher.hash(formData.password)
#     return {"hashed_password": hashed}


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.perf_counter()
#     response = await call_next(request)
#     process_time = time.perf_counter() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response


"""next_id = 0


@app.get("/users")
async def get_users(name: str | None = None):
    if name:
        result = []

        for user in users:
            if user["name"].lower() == name.lower():
                result.append(user)

        return result

    return users


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user

    

@app.post("/users")
async def create_user(user: User):
    global next_id

    new_user = {
        "id": next_id,
        "name": user.name,
        "age": user.age,
        "email": user.email
    }

    users.append(new_user)
    next_id += 1

    return new_user


@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    for existing_user in users:
        if existing_user["id"] == user_id:
            existing_user["name"] = user.name
            existing_user["age"] = user.age
            existing_user["email"] = user.email

            return existing_user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)

            return {"Пользователь удалён"}"""

"""@app.post("/TVseries")
async def TV_series(
    tvseries_data: Annotated[TvseriesSchema, Body()],
    db_conn: AsyncSession = Depends(get_session),
):
    new_tvseries = Tvseries(name=tvseries_data.name, const_series=tvseries_data.const_series, length_series=tvseries_data.length_series)
    db_conn.add(new_tvseries)

    await db_conn.commit()

    return {"status": "application is running"}"""


# @app.post("/genre")
# async def read_root(
#     movie_data: Annotated[GenreSchema, Body()],
#     db_conn: AsyncSession = Depends(get_session),
# ):
#     new_genre = Genre(name=movie_data.genre, movie_id=movie_data.movie_id)
#     db_conn.add(new_genre)

#     await db_conn.commit()

#     return {"status": "application is running"}  # TODO: сделать текст информативным.

# @app.get("/filter")
# async def read_root(
#     movie_id: Annotated[int, Query()], db_conn: AsyncSession = Depends(get_session)
# ):
#     select_movie = select(Movie, Genre).join(Movie.genre).where(Movie.id == movie_id)

#     res = await db_conn.execute(select_movie)

#     for movie, genre in res.all():
#         print(movie.name, "-", genre.name)
#     print(res.all())

#     return {"RESULT": movie.name}


# if __name__ == "__main__":
#     asyncio.run(init_models())