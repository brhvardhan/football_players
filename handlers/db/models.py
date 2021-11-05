# This file contains the pydantic models
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