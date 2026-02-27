from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from .service import UomService
from .schemas import UomCreate, UomUpdate, UomOut

router = APIRouter(prefix="/api/uom", tags=["UOM Master"])
svc = UomService()

@router.post("", response_model=UomOut)
def create_uom(payload: UomCreate, db: Session = Depends(get_db)):
    return svc.create(db, payload)

@router.get("/{id}", response_model=UomOut)
def get_uom(id: int, db: Session = Depends(get_db)):
    return svc.get(db, id)

@router.get("", response_model=list[UomOut])
def list_uom(q: str | None = Query(None), skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return svc.list(db, q, skip, limit)

@router.put("/{id}", response_model=UomOut)
def update_uom(id: int, payload: UomUpdate, db: Session = Depends(get_db)):
    return svc.update(db, id, payload)