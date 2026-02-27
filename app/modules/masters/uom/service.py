from sqlalchemy.orm import Session
from fastapi import HTTPException
from .repo import UomRepo
from .models import Uom
from .schemas import UomCreate, UomUpdate

class UomService:
    def __init__(self):
        self.repo = UomRepo()

    def create(self, db: Session, data: UomCreate):
        if self.repo.get_by_name(db, data.name):
            raise HTTPException(409, "UOM already exists")
        return self.repo.create(db, Uom(**data.model_dump()))

    def get(self, db: Session, id: int):
        obj = self.repo.get_by_id(db, id)
        if not obj:
            raise HTTPException(404, "UOM not found")
        return obj

    def list(self, db: Session, q: str | None, skip: int, limit: int):
        return self.repo.list(db, q, skip, limit)

    def update(self, db: Session, id: int, data: UomUpdate):
        obj = self.get(db, id)
        patch = data.model_dump(exclude_unset=True)
        if "name" in patch:
            existing = self.repo.get_by_name(db, patch["name"])
            if existing and existing.id != id:
                raise HTTPException(409, "UOM name already used")
        for k, v in patch.items():
            setattr(obj, k, v)
        return self.repo.update(db, obj)

    def get_or_create_by_name(self, db: Session, name: str):
        name = name.strip()
        obj = self.repo.get_by_name(db, name)
        if obj:
            return obj
        return self.repo.create(db, Uom(name=name, is_active=True))