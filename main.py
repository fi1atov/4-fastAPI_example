from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from sqlalchemy.future import select
from sqlalchemy import update

import models
from models import Recept
import schemas
from database import engine, session


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.get("/")
async def read_index():
    return FileResponse('static/index.html')


@app.post('/add_recept', response_model=schemas.ReceptOut, status_code=201)
async def add_recepts(recept: schemas.ReceptIn) -> Recept:
    new_recept = Recept(**recept.dict())
    async with session.begin():
        session.add(new_recept)
        await session.commit()
    return new_recept


@app.get('/recepts', response_model=List[schemas.ReceptOut])
async def recepts() -> List[Recept]:
    async with session.begin():
        res = await session.execute(select(Recept).order_by(Recept.count_views.desc(), Recept.time_cook))
        await session.commit()
    return res.scalars().all()


@app.get('/recept/{rec_id}', response_model=List[schemas.ReceptOut])
async def recept(rec_id: int) -> List[Recept]:
    async with session.begin():
        # Получить count_views рецепта из базы
        views = await session.execute(select(Recept.count_views).where(Recept.id == rec_id))
        # Увеличить его на 1
        views = views.scalars().one() + 1
        # Проапдейтить запись
        await session.execute(update(Recept).where(Recept.id == rec_id).values(count_views=views))
        # А теперь показываем информацию пользователю
        res = await session.execute(select(Recept).where(Recept.id == rec_id))
        await session.commit()
    return res.scalars().all()


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host='127.0.0.1')
