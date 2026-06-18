from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, crud
from ..database import get_db
from ..security import get_current_user, require_role

router = APIRouter(prefix="/appointments", tags=["预约"])


@router.post("/", response_model=schemas.Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.create_appointment(db, client_id=current_user.id, lawyer_id=appointment.lawyer_id, title=appointment.title, description=appointment.description, appointment_type=appointment.appointment_type, appointment_date=appointment.appointment_date, start_time=appointment.start_time, end_time=appointment.end_time, location=appointment.location, meeting_link=appointment.meeting_link, appointment_time=appointment.appointment_time)


@router.get("/", response_model=List[schemas.Appointment])
def get_my_appointments(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.get_user_appointments(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{appointment_id}", response_model=schemas.Appointment)
def get_appointment(
    appointment_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    appointment = crud.get_appointment(db, appointment_id=appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="预约不存在")
    if appointment.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权查看")
    return appointment


@router.put("/{appointment_id}", response_model=schemas.Appointment)
def update_appointment_status(
    appointment_id: int,
    status_update: schemas.AppointmentUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    appointment = crud.get_appointment(db, appointment_id=appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="预约不存在")
    if appointment.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改")
    return crud.update_appointment(db, appointment_id=appointment_id, **status_update.model_dump(exclude_unset=True))
