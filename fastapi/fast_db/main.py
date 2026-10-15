from fastapi import FastAPI, Depends, Body, Query
from .db.main import get_session, init_models
from .db.models import Movie, Genre
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy import select, update, delete
import asyncio

app = FastAPI()

@app.on_event('startup')
async def startup():
    await init_models()



class MovieSchema(BaseModel):
    name: str
    length_min: int

class TvseriesSchema(BaseModel):
    name: str
    const_series: int
    length_series: int

class GenreSchema(BaseModel):
    genre: str
    movie_id: int


@app.post("/movie")
async def read_root(
    movie_data: Annotated[MovieSchema, Body()],
    db_conn: AsyncSession = Depends(get_session),
):
    new_movie = Movie(name=movie_data.name, length=movie_data.length_min)
    db_conn.add(new_movie)

    await db_conn.commit()

    return {"status": "application is running"}

"""@app.post("/TVseries")
async def TV_series(
    tvseries_data: Annotated[TvseriesSchema, Body()],
    db_conn: AsyncSession = Depends(get_session),
):
    new_tvseries = Tvseries(name=tvseries_data.name, const_series=tvseries_data.const_series, length_series=tvseries_data.length_series)
    db_conn.add(new_tvseries)

    await db_conn.commit()

    return {"status": "application is running"}"""

@app.post("/genre")
async def read_root(
    movie_data: Annotated[GenreSchema, Body()],
    db_conn: AsyncSession = Depends(get_session),
):
    new_genre = Genre(name=movie_data.genre, movie_id=movie_data.movie_id)
    db_conn.add(new_genre)

    await db_conn.commit()

    return {"status": "application is running"}


@app.put("/")
async def read_root(
    movie_id: Annotated[int, Query],
    movie_data: Annotated[MovieSchema, Body()],
    db_conn: AsyncSession = Depends(get_session),
):
    update_movie = update(Movie)

    new_data = await db_conn.execute(update_movie, [{"id": movie_id, "name": movie_data.name, "lengtg": movie_data.length_min}],)

    await db_conn.commit()

    return {"Обновлено": str(new_data.all())}


@app.delete("/")
async def read_root(
    movie_id: Annotated[int, Query()], db_conn: AsyncSession = Depends(get_session)
):
    delete_movie = delete(Movie).where(Movie.id == movie_id)

    await db_conn.execute(delete_movie)

    await db_conn.commit()

    return {"Result": "ok"}  #Не удаляется фильм, если есть зависимость с таблицей жанров


@app.get("/filter")
async def read_root(
    movie_id: Annotated[int, Query()], db_conn: AsyncSession = Depends(get_session)
):
    select_movie = select(Movie, Genre).join(Movie.genre).where(Movie.id == movie_id)
    
    res = await db_conn.execute(select_movie)
    
    for movie, genre in res.all():
        print(movie.name, "-", genre.name)
    print(res.all())
    
    return {"RESULT": movie.name}


if __name__ == "__main__":
    asyncio.run(init_models())

    
