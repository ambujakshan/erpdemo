from fastapi import HTTPException
from sqlalchemy.orm import Session
from .repo import HsnRepo
from .models import Hsn
from .schemas import HsnCreate, HsnUpdate

class HsnService:
    def __init__(self):
        self.repo = HsnRepo()

    def create(self, db: Session, data: HsnCreate):
        if self.repo.get_by_code(db, data.code):
            raise HTTPException(409, "HSN/SAC already exists")
        return self.repo.create(db, Hsn(**data.model_dump()))

    def get(self, db: Session, id: int):
        obj = self.repo.get_by_id(db, id)
        if not obj:
            raise HTTPException(404, "HSN/SAC not found")
        return obj

    def list(self, db: Session, q: str | None, skip: int, limit: int):
        return self.repo.list(db, q, skip, limit)

    def update(self, db: Session, id: int, data: HsnUpdate):
        obj = self.get(db, id)
        patch = data.model_dump(exclude_unset=True)

        if "code" in patch:
            existing = self.repo.get_by_code(db, patch["code"])
            if existing and existing.id != id:
                raise HTTPException(409, "HSN/SAC code already used")

        for k, v in patch.items():
            setattr(obj, k, v)
        return self.repo.update(db, obj)

    def get_or_create_by_code(self, db: Session, code: str, is_service: bool = False):
        code = code.strip()
        obj = self.repo.get_by_code(db, code)
        if obj:
            return obj
        return self.repo.create(db, Hsn(code=code, is_service=is_service, is_active=True))