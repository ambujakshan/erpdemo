from pydantic import BaseModel, Field
from typing import Optional

class UomCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    code: Optional[str] = Field(None, max_length=20)
    is_active: bool = True

class UomUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    code: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None

class UomOut(BaseModel):
    id: int
    name: str
    code: Optional[str]
    is_active: bool
    class Config:
        from_attributes = True