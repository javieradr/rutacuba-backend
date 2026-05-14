from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Van
from schemas import VanResponse
from dependencies import get_current_user
from models import User

router = APIRouter(prefix="/vans", tags=["Minivans"])

@router.get("/", response_model=List[VanResponse])
def list_active_vans(db: Session = Depends(get_db)):
    """Get all active vans (public endpoint)"""
    
    vans = db.query(Van).filter(Van.is_active == True).all()
    return [VanResponse.model_validate(van) for van in vans]

@router.get("/{van_id}", response_model=VanResponse)
def get_van(van_id: int, db: Session = Depends(get_db)):
    """Get van details"""
    
    van = db.query(Van).filter(Van.id == van_id).first()
    if not van:
        raise HTTPException(status_code=404, detail="Minivan no encontrada")
    
    return VanResponse.model_validate(van)
