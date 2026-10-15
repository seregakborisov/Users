from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from .base import Base


class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    length = Column(Integer)

    genre = relationship("Genre", back_populates="movie")

"""class Tvseries(Base):
    __tablename__ = "TVseies"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    const_series = Column(Integer)
    length_series = Column(Integer)

    genre = relationship("Genre", back_populates="tvseries")"""

class Genre(Base):
    __tablename__ = "Genre"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False)
    movie_id = mapped_column(ForeignKey("movie.id"), nullable=False)

    movie = relationship("Movie", back_populates="genre")
