from concurrent.futures import ThreadPoolExecutor
from fastapi import Depends, FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import time
import threading

import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import main
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import uuid  
import json

from functions import create_video, long_task
from pydantic import BaseModel


main.load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


VIDEO_FOLDER = 'vids'
if not os.path.exists(VIDEO_FOLDER):
    os.makedirs(VIDEO_FOLDER)

s3_bucket = 'bajttv'
s3_client = boto3.client('s3')


DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# task status memory list because mutable, and can be passed as reference
task_status_memory = [{}]


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


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/submit_data')
async def submit_data(data: UserData, db: Session = Depends(get_db)):
    new_data = UserDataDB(
        username=data.username,
        vid_name=data.vid_name,
        score=data.score,
        pause_count=data.pause_count,
        play_time=data.play_time
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"message": "Data submitted successfully", "data": new_data}


@app.get('/hello')
async def hello():
    return {"message": "Hello from the server!"}


@app.post('/upload_pdf')
async def upload_pdf(background_tasks: BackgroundTasks, pdf: UploadFile = File(...)):
    if not pdf.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDFs are allowed.")

    file_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await pdf.read())

    # create_video(file_path)
    
    task_id = str(uuid.uuid4())
    task_status_memory[0][task_id] = "PDF Uploaded"
    
    # background_tasks.add_task(long_task, task_id, task_status_memory)
    try:
        background_tasks.add_task(create_video, file_path, task_id, task_status_memory)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Someting wrong with generation."
        )
    
    return {"task_id": task_id}

    # return {"message": "PDF uploaded successfully", "file": pdf.filename}


@app.get('/get_videos')
async def get_videos():

    try:
        
        response = s3_client.list_objects_v2(Bucket=s3_bucket)
        files = [obj['Key'] for obj in response.get('Contents', [])]
        return files
    except Exception as e:
        raise HTTPException(
            status_code=500, detail='Error reading video directory from S3')


@app.get('/get_video/{filename}')
async def get_video(filename: str):

    try:
        
        if not os.path.exists("vids/" + filename):
            s3_client.download_file(s3_bucket, filename, "vids/" + filename)
        return FileResponse("vids/" + filename)
    except NoCredentialsError:
        raise HTTPException(
            status_code=403, detail="Credentials not available")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="File not found")


@app.get('/get_all_data')
async def get_all_data(db: Session = Depends(get_db)):
    data = db.query(UserDataDB).all()
    return data


@app.get("/check-task-status/{task_id}")
async def check_task_status(task_id: str):
    status = task_status_memory[0].get(task_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": status}


@app.post("/start-task")
async def start_task(background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    task_status_memory[0][task_id] = "Creating Video"
    background_tasks.add_task(long_task, task_id, task_status_memory)
    return {"task_id": task_id}


class QuizRequest(BaseModel):
    video_name: str

@app.post("/get_quiz")
async def get_quiz(quiz_request: QuizRequest):
    try:
        with open('quiz_data.json') as f:
            quiz_data = json.load(f)
        
        # Search for the quiz corresponding to the video_name
        quiz = next((item['quiz'] for item in quiz_data if item['videoName'] == quiz_request.video_name), None)
        
        if quiz is None:
            raise HTTPException(status_code=404, detail="Quiz not found for the given video name")

        return {"quiz": quiz}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error reading quiz data")

def function_one():
    for i in range(5):
        print(f"Function One - Count: {i}")
        time.sleep(1)

def function_two():
    for i in range(5):
        print(f"Function Two - Count: {i}")
        time.sleep(1)


@app.get("/run-tasks")
def run_tasks():
    # Use ThreadPoolExecutor to run functions concurrently
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(function_one)
        executor.submit(function_two)
    
    return {"message": "Tasks are running concurrently"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
