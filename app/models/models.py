from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # "pm" or "researcher"
    is_active = Column(Boolean, default=True)

    # Relationship with requirements
    requirements = relationship("Requirement", back_populates="creator")
    feedbacks = relationship("Feedback", back_populates="researcher")

class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    priority = Column(String, default="Medium")  # "High", "Medium", "Low"
    business_goal = Column(Text)
    data_scope = Column(Text)
    expected_output = Column(String)
    deadline = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Scorecard metrics
    clarity_score = Column(Float, default=0.0)
    feasibility_score = Column(Float, default=0.0)
    completeness_score = Column(Float, default=0.0)
    
    # AI feedback
    ai_feedback = Column(Text)
    
    # Relationships
    creator = relationship("User", back_populates="requirements")
    feedbacks = relationship("Feedback", back_populates="requirement")

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id"))
    researcher_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    requirement = relationship("Requirement", back_populates="feedbacks")
    researcher = relationship("User", back_populates="feedbacks") 