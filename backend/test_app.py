import os

import pytest
from fastapi.testclient import TestClient

from backend.app import app

# backend/test_app.py

client = TestClient(app)

def test_hello_route():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from the server!"}

def test_upload_pdf_route():
    pdf_path = "test_files/test.pdf"
    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\n%...")
    
    with open(pdf_path, "rb") as pdf:
        response = client.post('/upload_pdf', files={"pdf": pdf})
    
    assert response.status_code == 200
    assert "task_id" in response.json()

def test_get_script_route():
    pdf_path = "test_files/test.pdf"
    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\n%...")
    
    with open(pdf_path, "rb") as pdf:
        response = client.post('/get_script', data={"slides": 5}, files={"pdf": pdf})
    
    assert response.status_code == 200
    assert "scripts" in response.json()

def test_generate_image_route():
    image_request = {
        "script": "Test script",
        "ind": 1,
        "processId": "test_process",
        "height": 720,
        "width": 1280
    }
    response = client.post('/generate_image', json=image_request)
    assert response.status_code == 200
    assert response.json() == {"status": "done"}

def test_generate_video_route():
    video_request = {
        "scripts": ["Test script 1", "Test script 2"],
        "processId": "test_process",
        "captions": ["Caption 1", "Caption 2"],
        "languages": ["en", "es"]
    }
    response = client.post('/generate_video', json=video_request)
    assert response.status_code == 200
    assert response.json() == {"status": "done"}

def test_get_videos_route():
    response = client.get('/get_videos')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_image_route():
    response = client.get('/get_image', params={"filename": "test_image.png"})
    assert response.status_code in [200, 404]

def test_get_video_route():
    response = client.get('/get_video/test_video.mp4')
    assert response.status_code in [200, 404]

def test_get_all_data_route():
    response = client.get('/get_all_data')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_quiz_route():
    response = client.get('/get_quiz', params={"video_name": "test_video"})
    assert response.status_code in [200, 404]

def test_check_task_status_route():
    response = client.get('/check_task_status/test_task_id')
    assert response.status_code in [200, 404]

def test_publish_to_youtube_route():
    request_data = {
        "title": "Test Video",
        "description": "Test Description",
        "tags": ["test", "video"],
        "categoryId": "22"
    }
    response = client.post('/publish_to_youtube', json=request_data)
    assert response.status_code in [200, 500]

def test_submit_video_data_route():
    video_data = {
        "username": "test_user",
        "vid_name": "test_video",
        "pause_count": 5,
        "play_time": 120
    }
    response = client.post('/submit_video_data', json=video_data)
    assert response.status_code == 200
    assert "message" in response.json()

def test_submit_score_data_route():
    score_data = {
        "username": "test_user",
        "vid_name": "test_video",
        "score": 95
    }
    response = client.post('/submit_score_data', json=score_data)
    assert response.status_code == 200
    assert "message" in response.json()