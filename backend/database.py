# database.py
import os

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(os.environ.get("NEON_DATABASE_URL"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class QuizRequest(BaseModel):
    video_name: str


class UserData(BaseModel):
    username: str
    vid_name: str
    score: int
    pause_count: int
    play_time: int


class UserDataDB(Base):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    vid_name = Column(String, index=True)
    score = Column(Integer)
    pause_count = Column(Integer)
    play_time = Column(Integer)

class QuizDataDB(Base):
    __tablename__ = "quiz_data"
    id = Column(Integer, primary_key=True, index=True)
    video_name = Column(String, index=True)
    question = Column(String)
    options = Column(String)  # Store options as a JSON string
    correct_answer = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
