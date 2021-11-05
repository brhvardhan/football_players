from typing import Optional
from fastapi import FastAPI
from fastapi.param_functions import Depends

from handlers.db.models import NewMember
from api.team.app import router as team_router
from api.players.app import router as player_router
from api.players.app import get_members_obj
from api.players.methods import MembersCRUD

app = FastAPI()

app.include_router(team_router,prefix="/team", tags=['team'])
app.include_router(player_router,prefix="/player", tags=['player'])

@app.post("/create_player", tags=['player'])
async def create_player(data: NewMember, memeber_obj:MembersCRUD = Depends(get_members_obj)):
    return await memeber_obj.add_member(data.name, data.age, data.team_name)
    
