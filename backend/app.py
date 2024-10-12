import asyncio
import json
import os
import random
import time
import uuid

import boto3
from botocore.exceptions import NoCredentialsError
from database import *
from dotenv import load_dotenv
from fastapi import (BackgroundTasks, Depends, FastAPI, File, Form,
                     HTTPException, Query, UploadFile)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from utils.functions import *
from utils.youtube import *

load_dotenv()
prepare_folders()

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
async def hello_route():
    return {"message": "Hello from the server!"}


@app.post('/upload_pdf')
async def upload_pdf_route(background_tasks: BackgroundTasks, pdf: UploadFile = File(...)):
    if not pdf.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDFs are allowed.")

    UPLOAD_FOLDER = 'uploads'
    file_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await pdf.read())

    task_id = str(uuid.uuid4())
    task_status_memory[0][task_id] = "PDF Uploaded"

    try:
        background_tasks.add_task(
            create_video, file_path, task_id, task_status_memory)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Something wrong with generation."
        )

    return {"task_id": task_id}

    # return {"message": "PDF uploaded successfully", "file": pdf.filename}


@app.post('/get_script')
async def get_script_route(slides: int = Form(...), pdf: UploadFile = File(...)):
    if not pdf.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDFs are allowed.")

    UPLOAD_FOLDER = 'uploads'
    file_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await pdf.read())

    scripts = await get_script_from_pdf(file_path, slides)

    return {"scripts": scripts}


@app.post('/generate_image')
async def generate_image_route(imageRequest: ImageRequest):
    try:
        if not imageRequest:
            raise HTTPException(
                status_code=400, detail="Invalid request. ImageRequest is required.")

        await generate_image(imageRequest.script, imageRequest.ind, imageRequest.processId, imageRequest.height, imageRequest.width)

        return {"status": "done"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error reading images")



@app.post('/generate_video')
async def generate_video_route(videoRequest: VideoRequest):
    try:
        if not videoRequest:
            raise HTTPException(
                status_code=400, detail="Invalid request. VideoRequest is required.")

        await generate_video(videoRequest.scripts, videoRequest.processId, videoRequest.captions, videoRequest.languages)
        return {"status": "done"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error reading videos")


@app.get('/get_videos')
async def get_videos_route():
    try:
        response = s3_client.list_objects_v2(Bucket=s3_bucket)
        files = [obj['Key'] for obj in response.get('Contents', [])]
        return files
    except Exception as e:
        raise HTTPException(
            status_code=500, detail='Error reading video directory from S3')


@app.get('/get_image')
async def get_image_route(filename: str = Query(..., description="The name of the image file")):
    try:
        return FileResponse("temp_imgs/" + filename)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="File not found")


@app.get('/get_video/{filename}')
async def get_video_route(filename: str):
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
async def get_all_data_route(db: Session = Depends(get_db)):
    data = db.query(UserDataDB).all()
    return data


# @app.post('/submit_data')
# async def submit_data_route(data: UserData, db: Session = Depends(get_db)):
#     new_data = UserDataDB(
#         username=data.username,
#         vid_name=data.vid_name,
#         score=data.score,
#         pause_count=data.pause_count,
#         play_time=data.play_time
#     )
#     db.add(new_data)
#     db.commit()
#     db.refresh(new_data)
#     return {"message": "Data submitted successfully", "data": new_data}


@app.get("/get_quiz")
# Take video_name from query parameters
async def get_quiz_route(video_name: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Query the database for the quiz corresponding to the video_name
        quiz_data = db.query(QuizDataDB).filter(
            QuizDataDB.video_name == video_name).all()

        if not quiz_data:
            raise HTTPException(
                status_code=404, detail="Quiz not found for the given video name")

        quiz = [{"question": item.question, "options": json.loads(
            item.options), "correctAnswer": item.correct_answer} for item in quiz_data]

        return {"quiz": quiz}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error reading quiz data")


@app.get("/check-task-status/{task_id}")
async def check_task_status_route(task_id: str):
    status = task_status_memory[0].get(task_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": status}

# Add this function to your FastAPI app
@app.post("/publish_to_youtube")
async def publish_to_youtube_route(request: dict):
    try:
        youtube = get_authenticated_service()
        video_id = initialize_upload(youtube, request)
        return {"message": "Video uploaded successfully", "video_id": video_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/submit_video_data')
# New route for pause_count and play_time
async def submit_video_data_route(data: VideoData, db: Session = Depends(get_db)):
    new_data = UserDataDB(
        username=data.username,
        vid_name=data.vid_name,
        pause_count=data.pause_count,
        play_time=data.play_time
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"message": "Video data submitted successfully", "data": new_data}


@app.post('/submit_score_data')
# New route for score
async def submit_score_data_route(data: ScoreData, db: Session = Depends(get_db)):
    new_data = UserDataDB(
        username=data.username,
        vid_name=data.vid_name,
        score=data.score
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"message": "Score data submitted successfully", "data": new_data}


@app.post('/create_user')
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return {"message": "User already exists", "user_id": existing_user.id}
    
    new_user = User(
        name=user.name,
        email=user.email,
        isAdmin=user.isAdmin
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}

@app.get('/get_video_id/{video_id}')
async def get_video_id_route(video_id: int, db: Session = Depends(get_db)):
    try:
        video_data = db.query(VideoDB).filter(VideoDB.id == video_id).first()
        if not video_data:
            raise HTTPException(status_code=404, detail="Video data not found")
        return {
            "id": video_data.id,
            "name": video_data.name,
            "languages": video_data.languages,
            "youtube_url": video_data.youtube_url,
            "thumbnail_url": video_data.thumbnail_url,
            "description": video_data.description,
            "duration": video_data.duration,
            "no_slides": video_data.no_slides,
            "scripts": video_data.scripts
        }
    except Exception as e:
        print(f"Error fetching video data: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching video data")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

