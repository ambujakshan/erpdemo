from fastapi import HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal

from .repo import ProductUomRepo
from .models import ProductUom

class ProductUomService:
    def __init__(self):
        self.repo = ProductUomRepo()

    def list_by_product(self, db: Session, product_id: int):
        return self.repo.list_by_product(db, product_id)

    def set_conversions_for_product(self, db: Session, product_id: int, rows: list[dict], base_uom_id: int):
        """
        rows: list of dicts with keys: uom_id, factor, is_sales, is_purchase, barcode, selling_price_excl_tax, purchase_price
        Enforces:
          - base_uom_id must exist with factor=1 and is_base=true
          - only one base row
        """
        if not base_uom_id:
            raise HTTPException(422, "base_uom_id required")

        # wipe old rows (simplest & safe for edit)
        self.repo.delete_all_for_product(db, product_id)

        # Ensure base row exists
        base_row = None
        for r in rows:
            if int(r["uom_id"]) == int(base_uom_id):
                base_row = r
                break

        if base_row is None:
            # auto add base row if not provided
            rows = [{"uom_id": base_uom_id, "factor": 1, "is_sales": True, "is_purchase": True}] + rows

        # Create rows, validate only one base
        base_count = 0
        for r in rows:
            uom_id = int(r["uom_id"])
            factor = Decimal(str(r.get("factor", 1)))
            if factor <= 0:
                raise HTTPException(422, "factor must be > 0")

            is_base = (uom_id == int(base_uom_id))
            if is_base:
                base_count += 1
                factor = Decimal("1")

            obj = ProductUom(
                product_id=product_id,
                uom_id=uom_id,
                factor=factor,
                is_base=is_base,
                is_sales=bool(r.get("is_sales", True)),
                is_purchase=bool(r.get("is_purchase", True)),
                barcode=r.get("barcode"),
                selling_price_excl_tax=r.get("selling_price_excl_tax"),
                purchase_price=r.get("purchase_price"),
            )
            self.repo.create(db, obj)

        if base_count != 1:
            raise HTTPException(422, "Exactly one base UOM must exist (base_uom_id).")

    def convert_to_base(self, qty: float, factor: float) -> float:
        # qty_in_base = qty * factor
        return float(Decimal(str(qty)) * Decimal(str(factor)))