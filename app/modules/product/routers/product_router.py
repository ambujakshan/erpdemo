from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.modules.product.schemas.product_schema import ProductCreate, ProductResponse
from app.modules.product.services.product_service import create_product, list_products

router = APIRouter(prefix="/products", tags=["Product"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductResponse)
def create(dto: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, dto)

@router.get("/", response_model=list[ProductResponse])
def list_all(db: Session = Depends(get_db)):
    return list_products(db)