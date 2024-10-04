import asyncio
import json
import os
import uuid
import random
import time
import httplib2
import http.client as httplib

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

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

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

# YouTube API constants
CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

# YouTube upload retry constants
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

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
async def get_quiz(quiz_request: QuizRequest, db: Session = Depends(get_db)):
    try:
        quiz_data = db.query(QuizDataDB).filter(QuizDataDB.video_name == quiz_request.video_name).all()

        if not quiz_data:
            raise HTTPException(
                status_code=404, detail="Quiz not found for the given video name")

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

def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE)
    storage = Storage("youtube-oauth2.json")
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))

def initialize_upload(youtube, options):
    body = dict(
        snippet=dict(
            title=options['title'],
            description=options['description'],
            tags=options['keywords'].split(",") if options['keywords'] else None,
            categoryId=options['category']
        ),
        status=dict(
            privacyStatus=options['privacyStatus']
        )
    )

    # Download the file from S3 if it doesn't exist locally
    local_file_path = f"vids/{options['file']}"
    if not os.path.exists(local_file_path):
        s3_client.download_file(s3_bucket, options['file'], local_file_path)

    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(local_file_path, chunksize=-1, resumable=True)
    )

    return resumable_upload(insert_request)

def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print(f"Video id '{response['id']}' was successfully uploaded.")
                    return response['id']
                else:
                    raise Exception("The upload failed with an unexpected response: %s" % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f"A retriable error occurred: {e}"

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                raise Exception("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print(f"Sleeping {sleep_seconds} seconds and then retrying...")
            time.sleep(sleep_seconds)

@app.post("/publish_to_youtube")
async def publish_to_youtube(request: dict):
    try:
        youtube = get_authenticated_service()
        video_id = initialize_upload(youtube, request)
        return {"message": "Video uploaded successfully", "video_id": video_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")