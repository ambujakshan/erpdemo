from fastapi import HTTPException
from sqlalchemy.orm import Session
from .repo import GstRateRepo
from .models import GstRate
from .schemas import GstRateCreate, GstRateUpdate

class GstRateService:
    def __init__(self):
        self.repo = GstRateRepo()

    def create(self, db: Session, data: GstRateCreate):
        if self.repo.get_by_rate_cat(db, data.rate, data.category):
            raise HTTPException(409, "GST rate already exists for category")
        return self.repo.create(db, GstRate(**data.model_dump()))

    def get(self, db: Session, id: int):
        obj = self.repo.get_by_id(db, id)
        if not obj:
            raise HTTPException(404, "GST rate not found")
        return obj

    def list(self, db: Session, q: str | None, skip: int, limit: int):
        return self.repo.list(db, q, skip, limit)

    def update(self, db: Session, id: int, data: GstRateUpdate):
        obj = self.get(db, id)
        patch = data.model_dump(exclude_unset=True)

        if "rate" in patch or "category" in patch:
            new_rate = patch.get("rate", float(obj.rate))
            new_cat = patch.get("category", obj.category)
            existing = self.repo.get_by_rate_cat(db, new_rate, new_cat)
            if existing and existing.id != id:
                raise HTTPException(409, "GST rate already exists for category")

        for k, v in patch.items():
            setattr(obj, k, v)
        return self.repo.update(db, obj)

    def get_or_create_rate(self, db: Session, rate: float, category: str = "TAXABLE"):
        obj = self.repo.get_by_rate_cat(db, rate, category)
        if obj:
            return obj
        return self.repo.create(db, GstRate(rate=rate, category=category, is_active=True))