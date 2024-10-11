# database.py
import os

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(os.environ.get("NEON_DATABASE_URL"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class VideoRequest(BaseModel):
    preocessId: str
    scripts: list
    captions: bool
    languages: list[str]

class ImageRequest(BaseModel):
    script: str
    ind: int
    processId: str
    height: int
    width: int

class QuizRequest(BaseModel):
    video_name: str


class UserData(BaseModel):
    username: str
    vid_name: str
    score: int
    pause_count: int
    play_time: int

class ScoreData(BaseModel):
    username: str
    vid_name: str
    score: int

class VideoData(BaseModel):
    username: str
    vid_name: str
    pause_count: int
    play_time: float


class Script(BaseModel):
    Title: str
    Script: str

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

class VideoDB(Base):
    __tablename__ = "videos_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    languages = Column(String)  # Store languages as a JSON string
    youtube_url = Column(String)
    thumbnail_url = Column(String)
    description = Column(String)
    duration = Column(Integer)
    no_slides = Column(Integer)
    scripts = Column(String)  # Store scripts as a JSON string
    

class UserCreate(BaseModel):
    name: str
    email: str
    isAdmin: bool = False

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    isAdmin = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
