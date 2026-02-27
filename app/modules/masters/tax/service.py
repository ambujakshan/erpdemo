from fastapi import HTTPException
from sqlalchemy.orm import Session
from .repo import TaxRepo
from .models import TaxMaster

class TaxService:
    def __init__(self):
        self.repo = TaxRepo()

    def create(self, db: Session, name: str, tax_type: str, gst_rate_id: int, is_active: bool = True):
        if self.repo.get_by_name(db, name):
            raise HTTPException(409, "Tax master already exists")
        obj = TaxMaster(name=name, tax_type=tax_type, gst_rate_id=gst_rate_id, is_active=is_active)
        return self.repo.create(db, obj)

    def get(self, db: Session, id: int):
        obj = self.repo.get_by_id(db, id)
        if not obj:
            raise HTTPException(404, "Tax master not found")
        return obj

    def list(self, db: Session, q: str | None, skip: int, limit: int):
        return self.repo.list(db, q, skip, limit)

    def update(self, db: Session, id: int, patch: dict):
        obj = self.get(db, id)
        if "name" in patch:
            existing = self.repo.get_by_name(db, patch["name"])
            if existing and existing.id != id:
                raise HTTPException(409, "Tax name already used")
        for k, v in patch.items():
            setattr(obj, k, v)
        return self.repo.update(db, obj)

    def get_or_create(self, db: Session, name: str, tax_type: str, gst_rate_id: int):
        name = name.strip()
        obj = self.repo.get_by_name(db, name)
        if obj:
            return obj
        return self.repo.create(db, TaxMaster(name=name, tax_type=tax_type, gst_rate_id=gst_rate_id, is_active=True))