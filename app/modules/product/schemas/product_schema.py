from pydantic import BaseModel
from decimal import Decimal

class ProductCreate(BaseModel):
    product_code: str
    product_name: str
    product_class: str
    product_type: str
    asset_type: str | None = None

    selling_price: Decimal
    cost_price: Decimal

    track_stock: bool = True
    batch_tracking: bool = False
    expiry_tracking: bool = False

class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True