from fastapi import APIRouter, Query
from sqlalchemy import func
from sqlalchemy.sql.expression import desc, select
from sqlalchemy.sql.sqltypes import Enum

from handlers.db.connect import async_session
from handlers.db.schema import Team, Member


router = APIRouter()

@router.get("/average_age")
async def get_average_age(order:str=Query('asc', enum=['asc','desc'], description='Order in Asc or Desc'), ):
    async with async_session() as session :
        async with session.begin():
            sql = select([Team.id, Team.name, func.avg(Member.age).label("avg")]).join(Member).group_by(Team.id)
            if order == "desc":
                sql = sql.order_by(desc("avg"))
            else:
                 sql = sql.order_by("avg")
            res = await session.execute(sql)
            result= res.fetchall()
            return result
