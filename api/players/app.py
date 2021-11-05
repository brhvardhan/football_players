from typing import Optional
from fastapi import APIRouter, status
from fastapi.param_functions import Depends

from handlers.db.connect import async_session
from handlers.db.models import UpdateMember
from .methods import MembersCRUD


async def get_members_obj():
    async with async_session() as session:
        async with session.begin():
            yield MembersCRUD(session)


router = APIRouter()


@router.get("/{id}")
async def get_player(id:int, member_obj: MembersCRUD = Depends(get_members_obj)):
        return await member_obj.get_member(id)

@router.put("/{id}")
async def update_player(id:int, details:UpdateMember, member_obj: MembersCRUD = Depends(get_members_obj)):
        return await member_obj.update_member(id, details.name, details.age, details.team_id)

@router.delete("/{id}")
async def delete_player(id:int, member_obj: MembersCRUD = Depends(get_members_obj)):
        return await member_obj.delete_member(id)