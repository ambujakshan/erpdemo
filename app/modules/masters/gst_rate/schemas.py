from pydantic import BaseModel, Field
from typing import Optional

class GstRateCreate(BaseModel):
    rate: float = Field(..., ge=0, le=100)
    category: str = Field("TAXABLE", max_length=30)
    is_active: bool = True

class GstRateUpdate(BaseModel):
    rate: Optional[float] = Field(None, ge=0, le=100)
    category: Optional[str] = Field(None, max_length=30)
    is_active: Optional[bool] = None

class GstRateOut(BaseModel):
    id: int
    rate: float
    category: str
    is_active: bool
    class Config:
        from_attributes = True