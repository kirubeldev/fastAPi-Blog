from sqlalchemy import Column, Integer, String, Text ,ForeignKey, TIMESTAMP, DateTime ,Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID , JSONB
import uuid
import enum
from datetime import datetime , timezone
from sqlalchemy.ext.mutable import MutableList

from database import Base

class User(Base):
    __tablename__ = "users"

    class Status_type(str , enum.Enum):
        PENDING = "pending"
        ACTIVE ="active"
        DEACTIVATED = "deactivated"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)
    register_OTP = Column(MutableList.as_mutable(JSONB), default=[])  
    forgot_passwod_OTP = Column(MutableList.as_mutable(JSONB), default=[])  
    otp_created_at = Column(TIMESTAMP, default=None)
    status =Column(Enum(Status_type) , nullable=False , default=Status_type.PENDING)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    blogs= relationship("Blog" , back_populates="userowner")



class Blog(Base):
    __tablename__="blogs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    title =Column(String, nullable=False , index=True)
    body =Column(String , nullable=False )
    owner_id= Column(UUID(as_uuid=True)  , ForeignKey("users.id") ,  nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    userowner= relationship("User" , back_populates="blogs")

