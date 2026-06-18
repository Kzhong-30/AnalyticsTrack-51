from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, crud
from ..models import DocumentType
from ..database import get_db
from ..security import get_current_user, require_role

router = APIRouter(prefix="/documents", tags=["文书"])


@router.get("/templates", response_model=List[schemas.DocumentTemplate])
def get_document_templates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_document_templates(db, skip=skip, limit=limit)


@router.get("/templates/{template_id}", response_model=schemas.DocumentTemplate)
def get_document_template(template_id: int, db: Session = Depends(get_db)):
    template = crud.get_document_template(db, template_id=template_id)
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")
    return template


@router.post("/generate", response_model=schemas.Document, status_code=status.HTTP_201_CREATED)
def generate_document(
    document_generate: schemas.DocumentGenerateRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    template = crud.get_document_template(db, template_id=document_generate.template_id)
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")
    generated_content = template.template_content
    for key, value in document_generate.variables.items():
        generated_content = generated_content.replace("{{" + key + "}}", str(value))
    return crud.create_document(
        db, user_id=current_user.id,
        title=template.name + " - 生成文档",
        file_path=f"generated/{template.name}_{current_user.id}.docx",
        document_type=template.document_type or DocumentType.OTHER,
        consultation_id=None,
    )


@router.get("/", response_model=List[schemas.Document])
def get_my_documents(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.get_lawyer_documents(db, lawyer_id=current_user.id, skip=skip, limit=limit)


@router.get("/{document_id}", response_model=schemas.Document)
def get_document(
    document_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    document = crud.get_document(db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="文书不存在")
    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权查看")
    return document
