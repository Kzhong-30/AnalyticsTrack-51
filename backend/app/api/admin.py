from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from .. import models, schemas, crud
from ..models import LawyerStatus
from ..database import get_db
from ..security import get_current_user, require_role

router = APIRouter(prefix="/admin", tags=["管理"])


@router.get("/stats", response_model=schemas.AdminStats)
def get_stats(
    current_admin: models.User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    return crud.get_stats(db)


@router.get("/lawyers", response_model=List[schemas.LawyerProfile])
def get_pending_lawyers(
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_admin: models.User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    if status_filter == "pending":
        return db.query(models.LawyerProfile).options(joinedload(models.LawyerProfile.user)).filter(models.LawyerProfile.status == LawyerStatus.PENDING).offset(skip).limit(limit).all()
    return crud.list_lawyers(db, skip=skip, limit=limit)


@router.put("/lawyers/{lawyer_id}/verify", response_model=schemas.LawyerProfile)
def verify_lawyer(
    lawyer_id: int,
    verify: schemas.LawyerVerify,
    current_admin: models.User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    lawyer = crud.get_lawyer_profile(db, lawyer_id=lawyer_id)
    if not lawyer:
        raise HTTPException(status_code=404, detail="律师不存在")
    return crud.update_lawyer_profile(db, profile_id=lawyer_id, **verify.model_dump(exclude_unset=True))


@router.get("/complaints", response_model=List[schemas.Complaint])
def get_complaints(
    skip: int = 0,
    limit: int = 100,
    current_admin: models.User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    return crud.get_complaints(db, skip=skip, limit=limit)


@router.put("/complaints/{complaint_id}", response_model=schemas.Complaint)
def handle_complaint(
    complaint_id: int,
    handle: schemas.ComplaintUpdate,
    current_admin: models.User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    complaint = crud.get_complaint(db, complaint_id=complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="投诉不存在")
    return crud.update_complaint(db, complaint_id=complaint_id, **handle.model_dump(exclude_unset=True))


@router.post("/knowledge", response_model=schemas.KnowledgeEntry, status_code=status.HTTP_201_CREATED)
def create_knowledge_entry(
    entry: schemas.KnowledgeEntryCreate,
    current_admin: models.User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    return crud.create_knowledge_entry(db, title=entry.title, content=entry.content, author_id=current_admin.id, category=entry.category, tags=entry.tags, is_published=entry.is_published)


@router.post("/document-templates", response_model=schemas.DocumentTemplate, status_code=status.HTTP_201_CREATED)
def create_document_template(
    template: schemas.DocumentTemplateCreate,
    current_admin: models.User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    return crud.create_document_template(db, name=template.name, template_content=template.template_content, description=template.description, document_type=template.document_type, category=template.category, variables=template.variables, is_active=template.is_active, created_by=current_admin.id)
