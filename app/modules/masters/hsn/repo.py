from sqlalchemy.orm import Session
from .models import Hsn

class HsnRepo:
    def get_by_id(self, db: Session, id: int):
        return db.query(Hsn).filter(Hsn.id == id).first()

    def get_by_code(self, db: Session, code: str):
        return db.query(Hsn).filter(Hsn.code == code.strip()).first()

    def list(self, db: Session, q: str | None, skip: int, limit: int):
        qry = db.query(Hsn)
        if q:
            qry = qry.filter(Hsn.code.ilike(f"%{q}%"))
        return qry.order_by(Hsn.code.asc()).offset(skip).limit(limit).all()

    def create(self, db: Session, obj: Hsn):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: Hsn):
        db.commit()
        db.refresh(obj)
        return obj