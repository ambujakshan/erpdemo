from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from .service import HsnService
from .schemas import HsnCreate, HsnUpdate, HsnOut

router = APIRouter(prefix="/api/hsn", tags=["HSN Master"])
svc = HsnService()

@router.post("", response_model=HsnOut)
def create(payload: HsnCreate, db: Session = Depends(get_db)):
    return svc.create(db, payload)

@router.get("/{id}", response_model=HsnOut)
def get_one(id: int, db: Session = Depends(get_db)):
    return svc.get(db, id)

@router.get("", response_model=list[HsnOut])
def list_all(q: str | None = Query(None), skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return svc.list(db, q, skip, limit)

@router.put("/{id}", response_model=HsnOut)
def update(id: int, payload: HsnUpdate, db: Session = Depends(get_db)):
    return svc.update(db, id, payload)