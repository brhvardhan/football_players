import asyncio
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.sql.expression import null
from sqlalchemy.types import Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from handlers.db.connect import engine

Base = declarative_base()

class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)

    # Relationships
    members = relationship("Member", back_populates="team")

class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    age = Column(Integer, nullable=False)
    team_id = Column(Integer, ForeignKey("team.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    team = relationship("Team", back_populates="members")
    


async def reset_database(Base):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(reset_database(Base))