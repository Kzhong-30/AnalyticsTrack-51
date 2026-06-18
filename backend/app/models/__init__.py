import enum
from datetime import datetime, time, date
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Enum, Boolean, Date, Time
from sqlalchemy.orm import relationship
from ..database import Base


class UserRole(str, enum.Enum):
    CLIENT = "client"
    LAWYER = "lawyer"
    ADMIN = "admin"


class ConsultationStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class AppointmentType(str, enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    PHONE = "phone"


class AppointmentStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class LawyerStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


class DocumentType(str, enum.Enum):
    CONTRACT = "contract"
    LEGAL_OPINION = "legal_opinion"
    POWER_OF_ATTORNEY = "power_of_attorney"
    COMPLAINT = "complaint"
    DEFENSE = "defense"
    OTHER = "other"


class LegalCategory(str, enum.Enum):
    CIVIL = "civil"
    CRIMINAL = "criminal"
    COMMERCIAL = "commercial"
    LABOR = "labor"
    FAMILY = "family"
    REAL_ESTATE = "real_estate"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    ADMINISTRATIVE = "administrative"
    OTHER = "other"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    avatar = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.CLIENT, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    lawyer_profile = relationship("LawyerProfile", back_populates="user", uselist=False)
    consultations_as_client = relationship("Consultation", back_populates="client", foreign_keys="Consultation.client_id")
    consultations_as_lawyer = relationship("Consultation", back_populates="lawyer", foreign_keys="Consultation.lawyer_id")
    appointments_as_client = relationship("Appointment", back_populates="client", foreign_keys="Appointment.client_id")
    appointments_as_lawyer = relationship("Appointment", back_populates="lawyer", foreign_keys="Appointment.lawyer_id")
    reviews_written = relationship("Review", back_populates="client", foreign_keys="Review.client_id")
    reviews_received = relationship("Review", back_populates="lawyer", foreign_keys="Review.lawyer_id")
    documents = relationship("Document", back_populates="user")
    complaints = relationship("Complaint", back_populates="user", foreign_keys="Complaint.user_id")


class LawyerProfile(Base):
    __tablename__ = "lawyer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    license_number = Column(String(50), unique=True, nullable=False)
    license_image = Column(String(255))
    firm_name = Column(String(100))
    years_of_experience = Column(Integer, default=0)
    bio = Column(Text)
    specialties = Column(String(255))
    category = Column(Enum(LegalCategory))
    consultation_fee = Column(Float, default=0.0)
    appointment_fee = Column(Float, default=0.0)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    status = Column(Enum(LawyerStatus), default=LawyerStatus.PENDING, nullable=False)
    verified_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="lawyer_profile")


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lawyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(Enum(LegalCategory))
    status = Column(Enum(ConsultationStatus), default=ConsultationStatus.PENDING, nullable=False)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    fee = Column(Float, default=0.0)
    paid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = relationship("User", back_populates="consultations_as_client", foreign_keys=[client_id])
    lawyer = relationship("User", back_populates="consultations_as_lawyer", foreign_keys=[lawyer_id])
    documents = relationship("Document", back_populates="consultation")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lawyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    appointment_type = Column(Enum(AppointmentType), default=AppointmentType.ONLINE, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING, nullable=False)
    appointment_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    location = Column(String(255))
    meeting_link = Column(String(255))
    fee = Column(Float, default=0.0)
    paid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = relationship("User", back_populates="appointments_as_client", foreign_keys=[client_id])
    lawyer = relationship("User", back_populates="appointments_as_lawyer", foreign_keys=[lawyer_id])
    review = relationship("Review", back_populates="appointment", uselist=False)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True, nullable=False)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lawyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    appointment = relationship("Appointment", back_populates="review")
    client = relationship("User", back_populates="reviews_written", foreign_keys=[client_id])
    lawyer = relationship("User", back_populates="reviews_received", foreign_keys=[lawyer_id])


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    consultation_id = Column(Integer, ForeignKey("consultations.id"))
    title = Column(String(200), nullable=False)
    document_type = Column(Enum(DocumentType))
    file_path = Column(String(255), nullable=False)
    file_size = Column(Integer)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="documents")
    consultation = relationship("Consultation", back_populates="documents")


class KnowledgeEntry(Base):
    __tablename__ = "knowledge_entries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(Enum(LegalCategory))
    tags = Column(String(255))
    author_id = Column(Integer, ForeignKey("users.id"))
    is_published = Column(Boolean, default=True)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    related_type = Column(String(50))
    related_id = Column(Integer)
    status = Column(String(20), default="pending")
    response = Column(Text)
    handled_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="complaints", foreign_keys=[user_id])


class DocumentTemplate(Base):
    __tablename__ = "document_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    document_type = Column(Enum(DocumentType))
    category = Column(Enum(LegalCategory))
    template_content = Column(Text, nullable=False)
    variables = Column(Text)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
