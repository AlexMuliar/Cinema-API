from sqlmodel import Field, SQLModel


class Movie(SQLModel, table=True):
    __tablename__ = 'movies'

    id: int = Field(default=None, primary_key=True)
    name: str
    duration_minutes: int
