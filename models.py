from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)
