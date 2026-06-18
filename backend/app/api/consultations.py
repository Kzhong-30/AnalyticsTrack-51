from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, crud
from ..database import get_db
from ..security import get_current_user, require_role

router = APIRouter(prefix="/consultations", tags=["咨询"])


@router.post("/", response_model=schemas.Consultation, status_code=status.HTTP_201_CREATED)
def create_consultation(
    consultation: schemas.ConsultationCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.create_consultation(db, client_id=current_user.id, lawyer_id=consultation.lawyer_id, title=consultation.title, description=consultation.description, category=consultation.category)


@router.get("/", response_model=List[schemas.Consultation])
def get_my_consultations(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.get_user_consultations(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{consultation_id}", response_model=schemas.Consultation)
def get_consultation(
    consultation_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    consultation = crud.get_consultation(db, consultation_id=consultation_id)
    if not consultation:
        raise HTTPException(status_code=404, detail="咨询不存在")
    if consultation.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权查看")
    return consultation


@router.put("/{consultation_id}", response_model=schemas.Consultation)
def update_consultation(
    consultation_id: int,
    consultation_update: schemas.ConsultationUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    consultation = crud.get_consultation(db, consultation_id=consultation_id)
    if not consultation:
        raise HTTPException(status_code=404, detail="咨询不存在")
    if consultation.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改")
    return crud.update_consultation(db, consultation_id=consultation_id, **consultation_update.model_dump(exclude_unset=True))


@router.post("/{consultation_id}/match", response_model=List[schemas.LawyerProfile])
def match_lawyers(
    consultation_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    consultation = crud.get_consultation(db, consultation_id=consultation_id)
    if not consultation:
        raise HTTPException(status_code=404, detail="咨询不存在")
    if consultation.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权操作")
    return crud.match_lawyers(db, category=consultation.category)
