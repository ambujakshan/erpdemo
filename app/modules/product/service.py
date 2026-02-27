from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.masters.uom.service import UomService
from app.modules.masters.hsn.service import HsnService
from app.modules.masters.gst_rate.service import GstRateService
from app.modules.masters.tax.service import TaxService

from app.modules.product_uom.service import ProductUomService

from .repo import ProductRepo
from .models import Product
from .schemas import ProductCreate

class ProductService:
    def __init__(self):
        self.repo = ProductRepo()
        self.uom_svc = UomService()
        self.hsn_svc = HsnService()
        self.gst_svc = GstRateService()
        self.tax_svc = TaxService()
        self.puom_svc = ProductUomService()

    def create(self, db: Session, data: ProductCreate):
        if self.repo.get_by_code(db, data.product_code):
            raise HTTPException(409, "Product code already exists")

        # ✅ Base UOM resolve
        if data.base_uom_id:
            base_uom = self.uom_svc.get(db, data.base_uom_id)
        elif data.base_uom_name:
            base_uom = self.uom_svc.get_or_create_by_name(db, data.base_uom_name)
        else:
            raise HTTPException(422, "base_uom_id or base_uom_name required")

        # HSN/SAC resolve
        if data.hsn_id:
            hsn = self.hsn_svc.get(db, data.hsn_id)
        elif data.hsn_code:
            is_service = data.hsn_is_service if data.hsn_is_service is not None else (data.product_type == "SERVICE")
            hsn = self.hsn_svc.get_or_create_by_code(db, data.hsn_code, is_service=is_service)
        else:
            raise HTTPException(422, "hsn_id or hsn_code required")

        # Tax resolve
        if data.tax_master_id:
            tax = self.tax_svc.get(db, data.tax_master_id)
        else:
            if not (data.tax_name and data.tax_type and data.gst_rate is not None):
                raise HTTPException(422, "tax_master_id OR (tax_name, tax_type, gst_rate) required")
            gst = self.gst_svc.get_or_create_rate(db, float(data.gst_rate), category=data.gst_category)
            tax = self.tax_svc.get_or_create(db, data.tax_name, data.tax_type, gst.id)

        # Create Product
        obj = Product(
            product_code=data.product_code,
            product_name=data.product_name,
            product_type=data.product_type,
            base_uom_id=base_uom.id,
            hsn_id=hsn.id,
            tax_master_id=tax.id,
            selling_price_excl_tax=data.selling_price_excl_tax,
            selling_price_incl_tax=data.selling_price_incl_tax,
            brand=data.brand,
            manufacturer=data.manufacturer,
            is_active=data.is_active,
        )
        obj = self.repo.create(db, obj)

        # ✅ Create product_uom conversions
        rows = []
        if data.uom_conversions:
            for c in data.uom_conversions:
                if c.uom_id:
                    u = self.uom_svc.get(db, c.uom_id)
                elif c.uom_name:
                    u = self.uom_svc.get_or_create_by_name(db, c.uom_name)
                else:
                    raise HTTPException(422, "Each uom_conversions item needs uom_id or uom_name")

                rows.append({
                    "uom_id": u.id,
                    "factor": c.factor,
                    "is_sales": c.is_sales,
                    "is_purchase": c.is_purchase,
                    "barcode": c.barcode,
                    "selling_price_excl_tax": c.selling_price_excl_tax,
                    "purchase_price": c.purchase_price,
                })

        # If no conversions provided, create only base conversion
        if not rows:
            rows = [{"uom_id": base_uom.id, "factor": 1, "is_sales": True, "is_purchase": True}]

        self.puom_svc.set_conversions_for_product(db, product_id=obj.id, rows=rows, base_uom_id=base_uom.id)

        return obj