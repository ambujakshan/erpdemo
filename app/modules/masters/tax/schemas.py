from pydantic import BaseModel, Field
from typing import Optional

class TaxCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    tax_type: str = Field(..., pattern="^(INTRA|INTER)$")
    gst_rate_id: int
    is_active: bool = True

class TaxUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=80)
    tax_type: Optional[str] = Field(None, pattern="^(INTRA|INTER)$")
    gst_rate_id: Optional[int] = None
    is_active: Optional[bool] = None

class TaxOut(BaseModel):
    id: int
    name: str
    tax_type: str
    gst_rate_id: int
    is_active: bool
    class Config:
        from_attributes = True