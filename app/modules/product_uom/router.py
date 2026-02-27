from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from .service import ProductUomService
from .schemas import ProductUomOut

router = APIRouter(prefix="/api/product-uom", tags=["Product UOM"])
svc = ProductUomService()

@router.get("/by-product/{product_id}", response_model=list[ProductUomOut])
def list_for_product(product_id: int, db: Session = Depends(get_db)):
    return svc.list_by_product(db, product_id)