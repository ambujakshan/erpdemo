from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from .service import TaxService
from .schemas import TaxCreate, TaxUpdate, TaxOut

router = APIRouter(prefix="/api/tax-master", tags=["Tax Master"])
svc = TaxService()

@router.post("", response_model=TaxOut)
def create(payload: TaxCreate, db: Session = Depends(get_db)):
    return svc.create(db, payload.name, payload.tax_type, payload.gst_rate_id, payload.is_active)

@router.get("/{id}", response_model=TaxOut)
def get_one(id: int, db: Session = Depends(get_db)):
    return svc.get(db, id)

@router.get("", response_model=list[TaxOut])
def list_all(q: str | None = Query(None), skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return svc.list(db, q, skip, limit)

@router.put("/{id}", response_model=TaxOut)
def update(id: int, payload: TaxUpdate, db: Session = Depends(get_db)):
    patch = payload.model_dump(exclude_unset=True)
    return svc.update(db, id, patch)