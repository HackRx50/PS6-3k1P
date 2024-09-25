import asyncio
import json
import os
import uuid

import boto3
from botocore.exceptions import NoCredentialsError
from database import *
from dotenv import load_dotenv
from fastapi import (BackgroundTasks, Depends, FastAPI, File, HTTPException,
                     UploadFile)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from functions import *
from sqlalchemy.orm import Session

load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


s3_bucket = 'bajttv'
s3_client = boto3.client('s3')


# task status memory list because mutable, and can be passed as reference
task_status_memory = [{}]


@app.get('/')
async def hello():
    return {"message": "Hello from the server!"}


@app.post('/upload_pdf')
async def upload_pdf(background_tasks: BackgroundTasks, pdf: UploadFile = File(...)):
    if not pdf.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDFs are allowed.")

    UPLOAD_FOLDER = 'uploads'
    file_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await pdf.read())

    # create_video(file_path)

    task_id = str(uuid.uuid4())
    task_status_memory[0][task_id] = "PDF Uploaded"

    # background_tasks.add_task(long_task, task_id, task_status_memory)
    try:
        background_tasks.add_task(
            create_video, file_path, task_id, task_status_memory)
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


@app.post("/get_quiz")
async def get_quiz(quiz_request: QuizRequest, db: Session = Depends(get_db)):  # Add db dependency
    try:
        # Query the database for the quiz corresponding to the video_name
        quiz_data = db.query(QuizDataDB).filter(QuizDataDB.video_name == quiz_request.video_name).all()

        if not quiz_data:
            raise HTTPException(
                status_code=404, detail="Quiz not found for the given video name")

        # Format the quiz data to return
        quiz = [{"question": item.question, "options": json.loads(item.options), "correctAnswer": item.correct_answer} for item in quiz_data]

        return {"quiz": quiz}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error reading quiz data")


@app.get("/check-task-status/{task_id}")
async def check_task_status(task_id: str):
    status = task_status_memory[0].get(task_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": status}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
