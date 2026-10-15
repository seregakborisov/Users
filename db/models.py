from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from db.base import Base


class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    length = Column(Integer)
    genre_id = mapped_column(
        ForeignKey("genre.id"),
        nullable=False,
    )

    genre = relationship("Genre", back_populates="movie", cascade="all, delete-orphan")


class TV_Series(Base):
    __tablename__ = "tv_seies"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    const_series = Column(Integer)
    length_series = Column(Integer)

    genre_id = mapped_column(
        ForeignKey("genre.id"),
        nullable=False,
    )

    genre = relationship("Genre", back_populates="tvseries", cascade="all, delete-orphan")


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False)

    movie = relationship("Movie", back_populates="genre")
    tv_series = relationship("TVSeries", back_populates="genre")
