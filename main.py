import uuid

import self
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from fastapi import FastAPI
from starlette import status
from starlette.responses import JSONResponse

# строка подключения
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# создаем движок SqlAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# создаем базовый класс для моделей
Base = declarative_base()


# создаем модель, объекты которой будут храниться в бд
class Rout(Base):
    __tablename__ = "routes"

    self.id = str(uuid.uuid4())
    self.length = Column(Integer)
    self.weight = Column(Integer)
    self.date_add = Column(Integer)
    self.date_del = Column(Integer)


# для поиска рулона в бд
def find_rout(id):
    for Rout in Base:
        if Rout.id == id:
            return Rout
    return None


# создаем таблицы
Base.metadata.create_all(bind=engine)

# приложение, которое ничего не делает
app = FastAPI()


# добавление рулона
@app.put("/coil./{rout_id}")
async def create_rout(rout_id: int, rout: Rout):
    return {"rout_id": rout_id, **rout.dict()}


# удаление рулона по id
@app.delete("/coil./{rout_id}")
async def delete_rout(id):
    rout = find_rout(id)

    if rout is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Рулон не найден"}
        )
    # если рулон найден, удаляем его
    rout.remove(Rout)
    return rout


# получение списка рулонов со склада
@app.get("/coil.")
def get_routes():
    return Rout


# получение статистики по рулонам за определённый период
@app.get("/coil/stats.")
def get_stats():
    return