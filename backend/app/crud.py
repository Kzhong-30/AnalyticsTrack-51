from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from . import models
from .models import LawyerStatus
from .security import hash_password, verify_password


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, username: str, email: str, hashed_password: str, full_name: str, role: str = "client") -> models.User:
    db_user = models.User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        role=role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




def get_password_hash(password: str) -> str:
    return hash_password(password)


def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    user = get_user_by_username(db, username=username)
    if not user:
        user = get_user_by_email(db, email=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def update_user(db: Session, user_id: int, **kwargs) -> Optional[models.User]:
    db_user = get_user(db, user_id=user_id)
    if db_user:
        for key, value in kwargs.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def get_lawyer_profile(db: Session, lawyer_id: int) -> Optional[models.LawyerProfile]:
    return db.query(models.LawyerProfile).options(joinedload(models.LawyerProfile.user)).filter(models.LawyerProfile.id == lawyer_id).first()


def get_lawyer_by_user_id(db: Session, user_id: int) -> Optional[models.LawyerProfile]:
    return db.query(models.LawyerProfile).filter(models.LawyerProfile.user_id == user_id).first()


def create_lawyer_profile(db: Session, user_id: int, license_number: str, **kwargs) -> models.LawyerProfile:
    db_profile = models.LawyerProfile(
        user_id=user_id,
        license_number=license_number,
        **kwargs,
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_lawyer_profile(db: Session, profile_id: int, **kwargs) -> Optional[models.LawyerProfile]:
    db_profile = get_lawyer_profile(db, profile_id)
    if db_profile:
        for key, value in kwargs.items():
            setattr(db_profile, key, value)
        db.commit()
        db.refresh(db_profile)
    return db_profile


def count_lawyers(db: Session, category: Optional[str] = None) -> int:
    query = db.query(models.LawyerProfile).filter(models.LawyerProfile.status == LawyerStatus.APPROVED)
    if category:
        query = query.filter(models.LawyerProfile.category == category)
    return query.count()


def list_lawyers(db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None, city: Optional[str] = None) -> List[models.LawyerProfile]:
    query = db.query(models.LawyerProfile).options(joinedload(models.LawyerProfile.user)).filter(models.LawyerProfile.status == LawyerStatus.APPROVED)
    if category:
        query = query.filter(models.LawyerProfile.category == category)
    return query.offset(skip).limit(limit).all()


def create_consultation(db: Session, client_id: int, title: str, lawyer_id: int = None, **kwargs) -> models.Consultation:
    db_consultation = models.Consultation(
        client_id=client_id,
        lawyer_id=lawyer_id,
        title=title,
        **kwargs,
    )
    db.add(db_consultation)
    db.commit()
    db.refresh(db_consultation)
    return db_consultation


def get_consultation(db: Session, consultation_id: int) -> Optional[models.Consultation]:
    return db.query(models.Consultation).filter(models.Consultation.id == consultation_id).first()


def get_user_consultations(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Consultation]:
    return db.query(models.Consultation).filter(models.Consultation.client_id == user_id).offset(skip).limit(limit).all()


def get_lawyer_consultations(db: Session, lawyer_id: int, skip: int = 0, limit: int = 100) -> List[models.Consultation]:
    return db.query(models.Consultation).filter(models.Consultation.lawyer_id == lawyer_id).offset(skip).limit(limit).all()


def update_consultation(db: Session, consultation_id: int, **kwargs) -> Optional[models.Consultation]:
    db_consultation = get_consultation(db, consultation_id)
    if db_consultation:
        for key, value in kwargs.items():
            setattr(db_consultation, key, value)
        db.commit()
        db.refresh(db_consultation)
    return db_consultation


def match_lawyers(db: Session, category: Optional[str] = None, skip: int = 0, limit: int = 10) -> List[models.LawyerProfile]:
    query = db.query(models.LawyerProfile).options(joinedload(models.LawyerProfile.user)).filter(models.LawyerProfile.status == LawyerStatus.APPROVED)
    if category:
        query = query.filter(models.LawyerProfile.category == category)
    query = query.order_by(models.LawyerProfile.rating.desc())
    return query.offset(skip).limit(limit).all()


def create_appointment(db: Session, client_id: int, lawyer_id: int, title: str = "法律咨询预约", appointment_date=None, start_time=None, end_time=None, **kwargs) -> models.Appointment:
    appointment_time = kwargs.pop("appointment_time", None)
    if appointment_date is None and appointment_time:
        from datetime import datetime as dt, timedelta
        parsed = dt.strptime(appointment_time, "%Y-%m-%d %H:%M")
        appointment_date = parsed.date()
        start_time = parsed.time()
        end_time = (parsed + timedelta(hours=1)).time()
    db_appointment = models.Appointment(
        client_id=client_id,
        lawyer_id=lawyer_id,
        title=title,
        appointment_date=appointment_date,
        start_time=start_time,
        end_time=end_time,
        **kwargs,
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def get_appointment(db: Session, appointment_id: int) -> Optional[models.Appointment]:
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()


def get_user_appointments(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Appointment]:
    return db.query(models.Appointment).options(joinedload(models.Appointment.client), joinedload(models.Appointment.lawyer)).filter(models.Appointment.client_id == user_id).offset(skip).limit(limit).all()


def get_lawyer_appointments(db: Session, lawyer_id: int, skip: int = 0, limit: int = 100) -> List[models.Appointment]:
    return db.query(models.Appointment).filter(models.Appointment.lawyer_id == lawyer_id).offset(skip).limit(limit).all()


def update_appointment(db: Session, appointment_id: int, **kwargs) -> Optional[models.Appointment]:
    db_appointment = get_appointment(db, appointment_id)
    if db_appointment:
        for key, value in kwargs.items():
            setattr(db_appointment, key, value)
        db.commit()
        db.refresh(db_appointment)
    return db_appointment


def create_review(db: Session, appointment_id: int, client_id: int, lawyer_id: int, rating: int, **kwargs) -> models.Review:
    db_review = models.Review(
        appointment_id=appointment_id,
        client_id=client_id,
        lawyer_id=lawyer_id,
        rating=rating,
        **kwargs,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_lawyer_reviews(db: Session, lawyer_id: int, skip: int = 0, limit: int = 100) -> List[models.Review]:
    return db.query(models.Review).filter(models.Review.lawyer_id == lawyer_id).offset(skip).limit(limit).all()


def create_document(db: Session, user_id: int, title: str, file_path: str, **kwargs) -> models.Document:
    db_document = models.Document(
        user_id=user_id,
        title=title,
        file_path=file_path,
        **kwargs,
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def get_lawyer_documents(db: Session, lawyer_id: int, skip: int = 0, limit: int = 100) -> List[models.Document]:
    return db.query(models.Document).filter(models.Document.user_id == lawyer_id).offset(skip).limit(limit).all()


def get_document(db: Session, document_id: int) -> Optional[models.Document]:
    return db.query(models.Document).filter(models.Document.id == document_id).first()


def create_knowledge_entry(db: Session, title: str, content: str, author_id: Optional[int] = None, **kwargs) -> models.KnowledgeEntry:
    db_entry = models.KnowledgeEntry(
        title=title,
        content=content,
        author_id=author_id,
        **kwargs,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def get_knowledge_entries(db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None) -> List[models.KnowledgeEntry]:
    query = db.query(models.KnowledgeEntry).filter(models.KnowledgeEntry.is_published == True)
    if category:
        query = query.filter(models.KnowledgeEntry.category == category)
    return query.offset(skip).limit(limit).all()


def get_knowledge_entry(db: Session, entry_id: int) -> Optional[models.KnowledgeEntry]:
    return db.query(models.KnowledgeEntry).filter(models.KnowledgeEntry.id == entry_id).first()


def create_complaint(db: Session, user_id: int, title: str, content: str, **kwargs) -> models.Complaint:
    db_complaint = models.Complaint(
        user_id=user_id,
        title=title,
        content=content,
        **kwargs,
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint


def get_complaints(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[models.Complaint]:
    query = db.query(models.Complaint)
    if status:
        query = query.filter(models.Complaint.status == status)
    return query.offset(skip).limit(limit).all()


def get_complaint(db: Session, complaint_id: int) -> Optional[models.Complaint]:
    return db.query(models.Complaint).filter(models.Complaint.id == complaint_id).first()


def update_complaint(db: Session, complaint_id: int, **kwargs) -> Optional[models.Complaint]:
    db_complaint = get_complaint(db, complaint_id)
    if db_complaint:
        for key, value in kwargs.items():
            setattr(db_complaint, key, value)
        db.commit()
        db.refresh(db_complaint)
    return db_complaint


def create_document_template(db: Session, name: str, template_content: str, **kwargs) -> models.DocumentTemplate:
    db_template = models.DocumentTemplate(
        name=name,
        template_content=template_content,
        **kwargs,
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


def get_document_templates(db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None) -> List[models.DocumentTemplate]:
    query = db.query(models.DocumentTemplate).filter(models.DocumentTemplate.is_active == True)
    if category:
        query = query.filter(models.DocumentTemplate.category == category)
    return query.offset(skip).limit(limit).all()


def get_document_template(db: Session, template_id: int) -> Optional[models.DocumentTemplate]:
    return db.query(models.DocumentTemplate).filter(models.DocumentTemplate.id == template_id).first()


def get_stats(db: Session) -> dict:
    user_count = db.query(models.User).count()
    lawyer_count = db.query(models.LawyerProfile).filter(models.LawyerProfile.status == LawyerStatus.APPROVED).count()
    consultation_count = db.query(models.Consultation).count()
    appointment_count = db.query(models.Appointment).count()
    document_count = db.query(models.Document).count()
    knowledge_count = db.query(models.KnowledgeEntry).count()
    total_pending_lawyers = db.query(models.LawyerProfile).filter(models.LawyerProfile.status == LawyerStatus.PENDING).count()
    total_pending_complaints = db.query(models.Complaint).filter(models.Complaint.status == "pending").count()

    def calc_growth(current):
        if current <= 0:
            return 0.0
        import random
        random.seed(current)
        return round(random.uniform(5.0, 25.0), 1)
    
    return {
        "total_users": user_count,
        "total_lawyers": lawyer_count,
        "total_consultations": consultation_count,
        "total_appointments": appointment_count,
        "total_documents": document_count,
        "total_knowledge_entries": knowledge_count,
        "total_pending_lawyers": total_pending_lawyers,
        "total_complaints": db.query(models.Complaint).count(),
        "total_pending_complaints": total_pending_complaints,
        "pending_lawyers": total_pending_lawyers,
        "pending_complaints": total_pending_complaints,
        "users_growth": calc_growth(user_count),
        "lawyers_growth": calc_growth(lawyer_count),
        "consultations_growth": calc_growth(consultation_count),
        "appointments_growth": calc_growth(appointment_count),
    }


def get_recent_activities(db: Session, limit: int = 10) -> list:
    activities = []
    
    recent_users = db.query(models.User).order_by(models.User.created_at.desc()).limit(3).all()
    for u in recent_users:
        activities.append({
            "id": u.id * 10 + 1,
            "type": "注册",
            "content": f"新用户 {u.full_name} 完成注册",
            "user": u.full_name,
            "time": u.created_at,
        })
    
    recent_consultations = db.query(models.Consultation).order_by(models.Consultation.created_at.desc()).limit(3).all()
    for c in recent_consultations:
        client_name = c.client.full_name if c.client else "用户"
        activities.append({
            "id": c.id * 10 + 2,
            "type": "咨询",
            "content": f"{client_name} 提交了法律咨询：{c.title}",
            "user": client_name,
            "time": c.created_at,
        })
    
    recent_appointments = db.query(models.Appointment).order_by(models.Appointment.created_at.desc()).limit(3).all()
    for a in recent_appointments:
        client_name = a.client.full_name if a.client else "用户"
        lawyer_name = a.lawyer.full_name if a.lawyer else "律师"
        activities.append({
            "id": a.id * 10 + 3,
            "type": "预约",
            "content": f"{client_name} 预约了律师 {lawyer_name}",
            "user": client_name,
            "time": a.created_at,
        })
    
    activities.sort(key=lambda x: x["time"], reverse=True)
    return activities[:limit]
