from sqlalchemy import Column, Integer, String, Text ,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)

    blogs= relationship("Blog" , back_populates="userowner")



class Blog(Base):
    __tablename__="blogs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    title =Column(String, nullable=False , index=True)
    body =Column(String , nullable=False )
    owner_id= Column(UUID(as_uuid=True)  , ForeignKey("users.id") ,  nullable=False)


    userowner= relationship("User" , back_populates="blogs")

