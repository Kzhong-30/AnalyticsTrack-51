from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db
from ..security import create_access_token, get_current_user, require_role

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="邮箱已注册")
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return crud.create_user(
        db=db,
        username=user.username,
        email=user.email,
        hashed_password=crud.get_password_hash(user.password),
        full_name=user.full_name,
        role=user.role,
    )


@router.post("/register/lawyer", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_lawyer(lawyer: schemas.LawyerCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=lawyer.email)
    if db_user:
        raise HTTPException(status_code=400, detail="邮箱已注册")
    db_user = crud.get_user_by_username(db, username=lawyer.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = crud.create_user(
        db=db,
        username=lawyer.username,
        email=lawyer.email,
        hashed_password=crud.get_password_hash(lawyer.password),
        full_name=lawyer.full_name,
        role=models.UserRole.LAWYER,
    )
    crud.create_lawyer_profile(
        db=db,
        user_id=user.id,
        license_number=lawyer.license_number,
        license_image=lawyer.license_image,
        firm_name=lawyer.firm_name,
        years_of_experience=lawyer.years_of_experience,
        bio=lawyer.bio,
        specialties=lawyer.specialties,
        category=lawyer.category,
        consultation_fee=lawyer.consultation_fee,
        appointment_fee=lawyer.appointment_fee,
    )
    return user
