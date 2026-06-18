from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, crud
from ..database import get_db
from ..security import get_current_user, require_role

router = APIRouter(prefix="/knowledge", tags=["知识库"])


@router.get("/", response_model=List[schemas.KnowledgeEntry])
def get_knowledge_entries(
    category: Optional[str] = Query(None, description="知识分类"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_knowledge_entries(db, category=category, skip=skip, limit=limit)


@router.get("/{entry_id}", response_model=schemas.KnowledgeEntry)
def get_knowledge_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = crud.get_knowledge_entry(db, entry_id=entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="知识条目不存在")
    return entry
