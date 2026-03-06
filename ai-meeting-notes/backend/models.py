from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Meeting(Base):
    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    transcript = Column(Text)
    summary = Column(Text)
    actions = Column(Text)  # could store JSON string of list
