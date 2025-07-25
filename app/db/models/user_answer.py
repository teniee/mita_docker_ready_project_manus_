from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    question_key = Column(String, nullable=False)
    answer_json = Column(String)
