from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db
from ..security import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["用户"])


@router.get("/me", response_model=schemas.User)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=schemas.User)
def update_me(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.update_user(db, user_id=current_user.id, **user_update.model_dump(exclude_unset=True))


@router.post("/complaints", response_model=schemas.Complaint, status_code=status.HTTP_201_CREATED)
def create_complaint(
    complaint: schemas.ComplaintCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.create_complaint(db, user_id=current_user.id, title=complaint.title, content=complaint.content, target_id=complaint.target_id, related_type=complaint.related_type, related_id=complaint.related_id)
