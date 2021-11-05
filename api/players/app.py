from typing import Optional
from fastapi import APIRouter, status
from fastapi.param_functions import Depends

from handlers.db.connect import async_session
from .methods import MembersCRUD


async def get_members_obj():
    async with async_session() as session:
        async with session.begin():
            yield MembersCRUD(session)


router = APIRouter()


@router.get("/{id}")
async def get_player(id:int, member_obj: MembersCRUD = Depends(get_members_obj)):
        return await member_obj.get_memeber(id)

@router.put("/{id}")
async def update_player(id:int, name: Optional[str]=None, age:Optional[int]=None, team_id:Optional[int]=None, member_obj: MembersCRUD = Depends(get_members_obj)):
        return await member_obj.update_member(id, name, age, team_id)

@router.delete("/{id}")
async def delete_player(id:int, member_obj: MembersCRUD = Depends(get_members_obj)):
        return await member_obj.delete_member(id)