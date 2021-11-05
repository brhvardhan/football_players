# This file contains the pydantic models
from typing import Optional
from pydantic import BaseModel, ValidationError, validator

class NewMember(BaseModel):
    name: str
    age: int
    team_name: str 

    @validator('age')
    def age_validator(cls, v):
        if v < 0:
            raise ValueError('Age should not be negative')
        return v

class UpdateMember(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    team_id: Optional[int] = None 

    @validator('age')
    def age_validator(cls, v):
        if v and v < 0:
            raise ValueError('Age should not be negative')
        return v

class AvgAgeOutput(BaseModel):
    id: int
    name: str
    avg : float