import re
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.expression import delete, desc, select
from starlette.responses import HTMLResponse, JSONResponse
from handlers.db.schema import Member, Team
from fastapi import status, HTTPException

class MembersCRUD():
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def add_member(self, name:str, age:int, team_name:str):
        member = Member(name = name, age= age)
        team_query =  await self.db_session.execute(select(Team).where(Team.name == team_name))
        team = team_query.scalars().one_or_none()
        if not team:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Team Name")
        member.team_id = team.id
        self.db_session.add(member)
        await self.db_session.commit()
        return member

    async def get_member(self, id:int) -> Member:
        query_obj = await self.db_session.execute(select(Member).where(Member.id == id).options(joinedload('team')))
        res = query_obj.scalars().one_or_none()
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
        return res
        
    async def update_member(self, id:int, name: Optional[str], age: Optional[int], team_id:Optional[int]):
        row = await self.get_member(id)
        if name:
            row.name = name
        if age:
           row.age = age
        if team_id:
            row.team_id = team_id

        await  self.db_session.commit()
        return JSONResponse(content={"detail":"Record Updated Successfully."}, status_code=status.HTTP_200_OK)

    async def delete_member(self, id: int):
        row = await self.get_member(id)
        await self.db_session.delete(row)
        return HTMLResponse(status_code=status.HTTP_204_NO_CONTENT)