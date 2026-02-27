from sqlalchemy.orm import Session
from .models import GstRate

class GstRateRepo:
    def get_by_id(self, db: Session, id: int):
        return db.query(GstRate).filter(GstRate.id == id).first()

    def get_by_rate_cat(self, db: Session, rate: float, category: str):
        return db.query(GstRate).filter(GstRate.rate == rate, GstRate.category == category).first()

    def list(self, db: Session, q: str | None, skip: int, limit: int):
        qry = db.query(GstRate)
        if q:
            qry = qry.filter(GstRate.category.ilike(f"%{q}%"))
        return qry.order_by(GstRate.rate.asc()).offset(skip).limit(limit).all()

    def create(self, db: Session, obj: GstRate):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: GstRate):
        db.commit()
        db.refresh(obj)
        return obj