from pydantic import BaseModel, Field
from typing import Optional

class HsnCreate(BaseModel):
    code: str = Field(..., min_length=2, max_length=16)
    description: Optional[str] = Field(None, max_length=255)
    is_service: bool = False
    is_active: bool = True

class HsnUpdate(BaseModel):
    code: Optional[str] = Field(None, min_length=2, max_length=16)
    description: Optional[str] = Field(None, max_length=255)
    is_service: Optional[bool] = None
    is_active: Optional[bool] = None

class HsnOut(BaseModel):
    id: int
    code: str
    description: Optional[str]
    is_service: bool
    is_active: bool
    class Config:
        from_attributes = True