from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from .service import ProductService
from .schemas import ProductCreate, ProductOut

router = APIRouter(prefix="/api/products", tags=["Product Master"])
svc = ProductService()

@router.post("", response_model=ProductOut)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return svc.create(db, payload)

@router.get("", response_model=list[ProductOut])
def list_products(q: str | None = Query(None), skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return svc.repo.list(db, q, skip, limit)