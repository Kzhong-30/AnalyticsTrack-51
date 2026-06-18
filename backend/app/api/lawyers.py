from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, crud
from ..database import get_db
from ..security import get_current_user, require_role

router = APIRouter(prefix="/lawyers", tags=["律师"])


@router.get("/", response_model=List[schemas.LawyerProfile])
def get_lawyers(
    category: Optional[str] = Query(None, description="律师分类"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.list_lawyers(db, category=category, skip=skip, limit=limit)


@router.get("/{lawyer_id}", response_model=schemas.LawyerProfile)
def get_lawyer(lawyer_id: int, db: Session = Depends(get_db)):
    lawyer = crud.get_lawyer_profile(db, lawyer_id=lawyer_id)
    if not lawyer:
        raise HTTPException(status_code=404, detail="律师不存在")
    return lawyer


@router.get("/{lawyer_id}/reviews", response_model=List[schemas.Review])
def get_lawyer_reviews(
    lawyer_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_lawyer_reviews(db, lawyer_id=lawyer_id, skip=skip, limit=limit)


@router.post("/{lawyer_id}/reviews", response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
def create_review(
    lawyer_id: int,
    review: schemas.ReviewCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.create_review(db, appointment_id=review.appointment_id, client_id=current_user.id, lawyer_id=lawyer_id, rating=review.rating, comment=review.comment)


@router.get("/me/profile", response_model=schemas.LawyerProfile)
def get_my_lawyer_profile(
    current_user: models.User = Depends(require_role("lawyer")),
    db: Session = Depends(get_db),
):
    profile = crud.get_lawyer_by_user_id(db, user_id=current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="律师资料不存在")
    return profile


@router.put("/me/profile", response_model=schemas.LawyerProfile)
def update_my_lawyer_profile(
    lawyer_update: schemas.LawyerProfileUpdate,
    current_user: models.User = Depends(require_role("lawyer")),
    db: Session = Depends(get_db),
):
    profile = crud.get_lawyer_by_user_id(db, user_id=current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="律师资料不存在")
    return crud.update_lawyer_profile(db, profile_id=profile.id, **lawyer_update.model_dump(exclude_unset=True))
