from pydantic import BaseModel, Field
from typing import Optional

class ProductUomCreate(BaseModel):
    product_id: int
    uom_id: int
    factor: float = Field(..., gt=0)
    is_base: bool = False
    is_sales: bool = True
    is_purchase: bool = True
    barcode: Optional[str] = None
    selling_price_excl_tax: Optional[float] = None
    purchase_price: Optional[float] = None

class ProductUomUpdate(BaseModel):
    factor: Optional[float] = Field(None, gt=0)
    is_base: Optional[bool] = None
    is_sales: Optional[bool] = None
    is_purchase: Optional[bool] = None
    barcode: Optional[str] = None
    selling_price_excl_tax: Optional[float] = None
    purchase_price: Optional[float] = None

class ProductUomOut(BaseModel):
    id: int
    product_id: int
    uom_id: int
    factor: float
    is_base: bool
    is_sales: bool
    is_purchase: bool
    barcode: Optional[str]
    selling_price_excl_tax: Optional[float]
    purchase_price: Optional[float]

    class Config:
        from_attributes = True