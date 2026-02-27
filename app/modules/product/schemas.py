from pydantic import BaseModel, Field
from typing import Optional

class ProductUomConversionIn(BaseModel):
    # allow either uom_id or uom_name
    uom_id: Optional[int] = None
    uom_name: Optional[str] = None

    factor: float = Field(..., gt=0)  # to base
    is_sales: bool = True
    is_purchase: bool = True
    barcode: Optional[str] = None
    selling_price_excl_tax: Optional[float] = None
    purchase_price: Optional[float] = None

class ProductCreate(BaseModel):
    product_code: str = Field(..., min_length=1, max_length=50)
    product_name: str = Field(..., min_length=1, max_length=150)
    product_type: str = Field(..., pattern="^(GOODS|SERVICE|FIXED_ASSET)$")

    # ✅ Base UOM (id or name)
    base_uom_id: Optional[int] = None
    base_uom_name: Optional[str] = None

    # HSN/SAC
    hsn_id: Optional[int] = None
    hsn_code: Optional[str] = None
    hsn_is_service: Optional[bool] = None

    # TaxMaster
    tax_master_id: Optional[int] = None
    tax_name: Optional[str] = None
    tax_type: Optional[str] = Field(None, pattern="^(INTRA|INTER)$")
    gst_rate: Optional[float] = None
    gst_category: str = "TAXABLE"

    selling_price_excl_tax: float = 0
    selling_price_incl_tax: float = 0
    brand: Optional[str] = None
    manufacturer: Optional[str] = None
    is_active: bool = True

    # ✅ Conversions (optional but recommended)
    # If not provided, system will create base conversion factor=1
    uom_conversions: Optional[list[ProductUomConversionIn]] = None

class ProductOut(BaseModel):
    id: int
    product_code: str
    product_name: str
    product_type: str

    base_uom_id: int
    hsn_id: int
    tax_master_id: int

    selling_price_excl_tax: float
    selling_price_incl_tax: float
    brand: Optional[str]
    manufacturer: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True