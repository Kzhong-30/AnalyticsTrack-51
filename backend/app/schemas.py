from datetime import datetime, date, time
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, model_validator

from .models import (
    UserRole,
    ConsultationStatus,
    AppointmentType,
    AppointmentStatus,
    LawyerStatus,
    DocumentType,
    LegalCategory,
)


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    full_name: str = Field(..., max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    avatar: Optional[str] = None
    role: UserRole = UserRole.CLIENT


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    avatar: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LawyerProfileBase(BaseModel):
    license_number: str = Field(..., max_length=50)
    license_image: Optional[str] = None
    firm_name: Optional[str] = Field(None, max_length=100)
    years_of_experience: int = 0
    bio: Optional[str] = None
    specialties: Optional[str] = Field(None, max_length=255)
    category: Optional[LegalCategory] = None
    consultation_fee: float = 0.0
    appointment_fee: float = 0.0


class LawyerProfileCreate(LawyerProfileBase):
    pass


class LawyerProfileUpdate(BaseModel):
    license_image: Optional[str] = None
    firm_name: Optional[str] = Field(None, max_length=100)
    years_of_experience: Optional[int] = None
    bio: Optional[str] = None
    specialties: Optional[str] = Field(None, max_length=255)
    category: Optional[LegalCategory] = None
    consultation_fee: Optional[float] = None
    appointment_fee: Optional[float] = None


class LawyerProfile(LawyerProfileBase):
    id: int
    user_id: int
    rating: float = 0.0
    review_count: int = 0
    status: LawyerStatus = LawyerStatus.PENDING
    verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    full_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def fill_user_fields(cls, values):
        obj = values
        if isinstance(values, dict):
            return values
        if hasattr(obj, "user") and obj.user is not None:
            if not getattr(obj, "full_name", None):
                values.full_name = obj.user.full_name
            if not getattr(obj, "username", None):
                values.username = obj.user.username
            if not getattr(obj, "email", None):
                values.email = obj.user.email
            if not getattr(obj, "phone", None):
                values.phone = obj.user.phone
            if not getattr(obj, "avatar", None):
                values.avatar = obj.user.avatar
        return values


class LawyerCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    license_number: str = Field(..., max_length=50)
    license_image: Optional[str] = None
    firm_name: Optional[str] = Field(None, max_length=100)
    years_of_experience: int = 0
    bio: Optional[str] = None
    specialties: Optional[str] = Field(None, max_length=255)
    category: Optional[LegalCategory] = None
    consultation_fee: float = 0.0
    appointment_fee: float = 0.0


class LawyerUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    avatar: Optional[str] = None
    firm_name: Optional[str] = Field(None, max_length=100)
    years_of_experience: Optional[int] = None
    bio: Optional[str] = None
    specialties: Optional[str] = Field(None, max_length=255)
    category: Optional[LegalCategory] = None
    consultation_fee: Optional[float] = None
    appointment_fee: Optional[float] = None


class Lawyer(BaseModel):
    id: int
    user_id: int
    username: str
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    avatar: Optional[str] = None
    license_number: str
    license_image: Optional[str] = None
    firm_name: Optional[str] = None
    years_of_experience: int = 0
    bio: Optional[str] = None
    specialties: Optional[str] = None
    category: Optional[LegalCategory] = None
    consultation_fee: float = 0.0
    appointment_fee: float = 0.0
    rating: float = 0.0
    review_count: int = 0
    status: LawyerStatus = LawyerStatus.PENDING
    verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LawyerVerify(BaseModel):
    status: LawyerStatus
    remark: Optional[str] = None


class ConsultationBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    category: Optional[LegalCategory] = None
    status: ConsultationStatus = ConsultationStatus.PENDING


class ConsultationCreate(ConsultationBase):
    lawyer_id: Optional[int] = None


class ConsultationUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    status: Optional[ConsultationStatus] = None


class Consultation(ConsultationBase):
    id: int
    client_id: int
    lawyer_id: int
    fee: float = 0.0
    paid: bool = False
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    client_name: Optional[str] = None
    lawyer_name: Optional[str] = None
    model_config = {"from_attributes": True}


class AppointmentBase(BaseModel):
    title: Optional[str] = Field("法律咨询预约", max_length=200)
    description: Optional[str] = None
    appointment_type: AppointmentType = AppointmentType.ONLINE
    appointment_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location: Optional[str] = Field(None, max_length=255)
    meeting_link: Optional[str] = Field(None, max_length=255)
    status: AppointmentStatus = AppointmentStatus.PENDING


class AppointmentCreate(AppointmentBase):
    lawyer_id: int
    appointment_time: Optional[str] = None


class AppointmentUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    appointment_type: Optional[AppointmentType] = None
    appointment_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location: Optional[str] = Field(None, max_length=255)
    meeting_link: Optional[str] = Field(None, max_length=255)
    status: Optional[AppointmentStatus] = None


class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus


class Appointment(AppointmentBase):
    id: int
    client_id: int
    lawyer_id: int
    fee: float = 0.0
    paid: bool = False
    created_at: datetime
    updated_at: datetime
    client_name: Optional[str] = None
    lawyer_name: Optional[str] = None
    lawyer_firm: Optional[str] = None
    model_config = {"from_attributes": True}


class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    lawyer_id: int
    appointment_id: int


class Review(ReviewBase):
    id: int
    client_id: int
    lawyer_id: int
    appointment_id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class DocumentBase(BaseModel):
    title: str = Field(..., max_length=200)
    document_type: DocumentType = DocumentType.OTHER
    description: Optional[str] = None


class DocumentCreate(DocumentBase):
    file_path: str


class Document(DocumentBase):
    id: int
    user_id: int
    file_path: str
    file_size: Optional[int] = 0
    consultation_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class DocumentGenerateRequest(BaseModel):
    template_id: int
    variables: Dict[str, Any]


class DocumentGenerate(DocumentGenerateRequest):
    pass


class KnowledgeEntryBase(BaseModel):
    title: str = Field(..., max_length=200)
    content: str
    category: Optional[LegalCategory] = None
    tags: Optional[str] = None
    is_published: bool = True


class KnowledgeEntryCreate(KnowledgeEntryBase):
    pass


class KnowledgeEntryUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = None
    category: Optional[LegalCategory] = None
    tags: Optional[str] = None
    is_published: Optional[bool] = None


class KnowledgeEntry(KnowledgeEntryBase):
    id: int
    author_id: Optional[int] = None
    view_count: int = 0
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class ComplaintBase(BaseModel):
    title: str = Field(..., max_length=200)
    content: str
    target_id: Optional[int] = None
    related_type: Optional[str] = Field(None, max_length=50)
    related_id: Optional[int] = None


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=50)
    response: Optional[str] = None


class ComplaintHandle(BaseModel):
    status: str
    response: Optional[str] = None


class Complaint(ComplaintBase):
    id: int
    user_id: int
    status: str = "pending"
    response: Optional[str] = None
    handled_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class DocumentTemplateBase(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    document_type: Optional[DocumentType] = None
    category: Optional[LegalCategory] = None
    template_content: str
    variables: Optional[str] = None
    is_active: bool = True


class DocumentTemplateCreate(DocumentTemplateBase):
    pass


class DocumentTemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    document_type: Optional[DocumentType] = None
    category: Optional[LegalCategory] = None
    template_content: Optional[str] = None
    variables: Optional[str] = None
    is_active: Optional[bool] = None


class DocumentTemplate(DocumentTemplateBase):
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class StatsResponse(BaseModel):
    total_users: int = 0
    total_lawyers: int = 0
    total_consultations: int = 0
    total_appointments: int = 0
    total_documents: int = 0
    total_knowledge_entries: int = 0


class AdminStats(StatsResponse):
    total_pending_lawyers: int = 0
    total_complaints: int = 0
    total_pending_complaints: int = 0
    pending_lawyers: int = 0
    pending_complaints: int = 0
    users_growth: float = 0.0
    lawyers_growth: float = 0.0
    consultations_growth: float = 0.0
    appointments_growth: float = 0.0


class ActivityItem(BaseModel):
    id: int
    type: str
    content: str
    user: str
    time: datetime


class LawyerListResponse(BaseModel):
    items: List[LawyerProfile]
    total: int
