from sqlalchemy.orm import Session
from .models import Product

class ProductRepo:
    def get_by_code(self, db: Session, code: str):
        return db.query(Product).filter(Product.product_code == code).first()

    def create(self, db: Session, obj: Product):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def list(self, db: Session, q: str | None, skip: int, limit: int):
        query = db.query(Product)
        if q:
            query = query.filter(Product.product_name.ilike(f"%{q}%"))
        return query.order_by(Product.id.desc()).offset(skip).limit(limit).all()