from sqlalchemy.orm import Session
from .models import ProductUom

class ProductUomRepo:
    def get_by_id(self, db: Session, id: int):
        return db.query(ProductUom).filter(ProductUom.id == id).first()

    def get_by_product_uom(self, db: Session, product_id: int, uom_id: int):
        return db.query(ProductUom).filter(
            ProductUom.product_id == product_id,
            ProductUom.uom_id == uom_id
        ).first()

    def list_by_product(self, db: Session, product_id: int):
        return db.query(ProductUom).filter(ProductUom.product_id == product_id).all()

    def create(self, db: Session, obj: ProductUom):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def delete_all_for_product(self, db: Session, product_id: int):
        db.query(ProductUom).filter(ProductUom.product_id == product_id).delete()
        db.commit()