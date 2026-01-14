from pydantic import BaseModel, Field
from typing import List, Optional


class TargetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    country: str = Field(min_length=1, max_length=120)
    notes: str = ""


class MissionCreate(BaseModel):
    targets: List[TargetCreate] = Field(min_length=1, max_length=3)


class MissionAssign(BaseModel):
    cat_id: int


class TargetUpdateNotes(BaseModel):
    notes: str


class TargetOut(BaseModel):
    id: int
    name: str
    country: str
    notes: str
    is_completed: bool

    class Config:
        from_attributes = True


class MissionOut(BaseModel):
    id: int
    cat_id: Optional[int]
    is_completed: bool
    targets: List[TargetOut]

    class Config:
        from_attributes = True
