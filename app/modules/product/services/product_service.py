from sqlalchemy.orm import Session
from app.modules.product.models.product import Product

def create_product(db: Session, dto):
    product = Product(**dto.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def list_products(db: Session):
    return db.query(Product).all()