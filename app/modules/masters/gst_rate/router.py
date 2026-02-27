from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from .service import GstRateService
from .schemas import GstRateCreate, GstRateUpdate, GstRateOut

router = APIRouter(prefix="/api/gst-rate", tags=["GST Rate Master"])
svc = GstRateService()

@router.post("", response_model=GstRateOut)
def create(payload: GstRateCreate, db: Session = Depends(get_db)):
    return svc.create(db, payload)

@router.get("/{id}", response_model=GstRateOut)
def get_one(id: int, db: Session = Depends(get_db)):
    return svc.get(db, id)

@router.get("", response_model=list[GstRateOut])
def list_all(q: str | None = Query(None), skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return svc.list(db, q, skip, limit)

@router.put("/{id}", response_model=GstRateOut)
def update(id: int, payload: GstRateUpdate, db: Session = Depends(get_db)):
    return svc.update(db, id, payload)