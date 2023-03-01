from pydantic import BaseModel


class BaseRecept(BaseModel):
    title: str
    count_views: int
    time_cook: int
    ingridients: str
    description: str


class ReceptIn(BaseModel):
    title: str
    time_cook: int
    ingridients: str
    description: str


class ReceptOut(BaseRecept):
    id: int

    class Config:
        orm_mode = True
