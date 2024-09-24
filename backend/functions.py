import io
import json
import os

import boto3
import requests
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips
from openai import OpenAI
from pdfminer.high_level import extract_text
from PIL import Image
import time
import asyncio


async def gen_and_save_image(prompt, file_path):
    image_bytes = await asyncio.to_thread(generate_image_from_text, prompt)  # Await the synchronous function
    dataBytesIO = io.BytesIO(image_bytes)
    img = Image.open(dataBytesIO)
    img.save(f"{file_path}.png")

async def gen_and_save_audio(script, file_path):
    client = OpenAI()

    # Run the synchronous call in a separate thread
    response = await asyncio.to_thread(client.audio.speech.create,
        model="tts-1",
        voice="shimmer",
        input=script
    )

    with open(f'{file_path}.mp3', 'wb') as f:
        f.write(response.content)

def generate_image_from_text(prompt):
    prompt = prompt + " araminta_illus illustration style"
    
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
    # API_URL = "https://api-inference.huggingface.co/models/alvdansen/softserve_anime"  # anime
    # API_URL = "https://api-inference.huggingface.co/modelsSebastianBodza/Flux_Aquarell_Watercolor_v2"

    headers = {"Authorization": "Bearer " + os.environ['FLUX_API_KEY']}
    data = {
        "inputs": "Soft Animation Style. "+prompt,
        "parameters": {
            "height": 400, "width": 800
        }
    }

    try:
        response = requests.post(
            API_URL, headers=headers, json=data, timeout=300)

        if response.status_code == 200:
            print("Image generation successful!")
            return response.content
        else:
            print(f"Error: {response.status_code}, {response.text}")
            error_message = f"Error {response.status_code}: {response.text}"
            return error_message.encode('utf-8')  
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}".encode('utf-8')


def combine_audio_and_video(name):

    audio_folder = "temp_auds"
    image_folder = "temp_imgs"

    audio_files = sorted([f for f in os.listdir(audio_folder) if f.endswith('.mp3') or f.endswith('.wav')])
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])

    video_clips = []

    for idx, audio_file in enumerate(audio_files):
        audio_path = os.path.join(audio_folder, audio_file)
        image_path = os.path.join(image_folder, f'{idx}.png')
        
        audio_clip = AudioFileClip(audio_path)
        
        image_clip = ImageClip(image_path).set_duration(audio_clip.duration)
        
        video_clip = image_clip.set_audio(audio_clip)
        
        video_clips.append(video_clip)

    final_video = concatenate_videoclips(video_clips)

    output_path = 'vids/' + name + '.mp4'
    final_video.write_videofile(output_path, fps=24)

    print("Video created successfully!")


async def create_video(file_path: str, task_id: str, tsm: list):
    START_TIME = time.time()
    
    name = os.path.basename(file_path).split(".")[0]
    
    print("\n", "creating video from the pdf", file_path)
    # get pdf content
    pdf_content = extract_text(file_path)
    
    tsm[0][task_id] = "Generating Script"

    print("\n", "hitting openai")
    # get openai slide breakdown
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": pdf_content + "\n\n" +
                "Break down the content into around 10 slides/pages and provide script for each slide. It must be in a json with just 2 keys, Script and Title, nothing else"},
        ]
    )
    ans = completion.choices[0].message.content
    print("\n", ans)

    ans = ans.strip("```")
    ans = ans.split("json")[1]
    ans = ans.replace("\n", "")

    parsed_slides = json.loads(ans)

    pages = parsed_slides

    print("\n", "pages", pages)
    script_compiled=""
    print("\n", "getting image prompts")
    for i, page in enumerate(pages):
        script_compiled=script_compiled+page["Script"]
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user",
                    "content": "give just a short suitable prompt to give to an image generator as if talking to a 10 year old to create an image for the slide with this content: " + page["Script"]}
            ]
        )
        ans = completion.choices[0].message.content
        page["image"] = ans


    ## Create quiz 
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Generate 10 simple quiz questions with 4 options to choose from, using the content of the script. Keep the questions things that customer should know about Bajaj Allianz. Script:"+ script_compiled + ". It must be in json format with 3 keys: question, options(4) and correctAnswer. Don't answer anything other than the json"}
        ]
    )
    quiz_ans = completion.choices[0].message.content

    quiz_ans = quiz_ans.strip("```")
    quiz_ans = quiz_ans.split("json")[1]
    quiz_ans = quiz_ans.replace("\n", "")

    parsed_quiz_ans = json.loads(quiz_ans)

    print('\n', "clearing temp folders")
    IMGS_FOLDER = 'temp_imgs'
    AUDS_FOLDER = 'temp_auds'
    if os.path.exists(IMGS_FOLDER):
        for file in os.listdir(IMGS_FOLDER):
            os.remove(os.path.join(IMGS_FOLDER, file))
    else:
        os.makedirs(IMGS_FOLDER)

    if os.path.exists(AUDS_FOLDER):
        for file in os.listdir(AUDS_FOLDER):
            os.remove(os.path.join(AUDS_FOLDER, file))
    else:
        os.makedirs(AUDS_FOLDER)

    tsm[0][task_id] = "Generating Images"
    print("\n", "getting images")

    N = len(pages)

    # creating images from prompts for all pages
    for i, page in enumerate(pages):
        try:
            print(page["image"])
            tsm[0][task_id] = f"Generating Image {i+1} of {N}"

            # Use gen_and_save_image instead of manual image generation
            await gen_and_save_image(page["image"], f"{IMGS_FOLDER}/{i}")
        except Exception as e:
            return e

    tsm[0][task_id] = "Generating Images Done."
    print("\n", "getting audios")
    
    # all audios from scripts
    for i, page in enumerate(pages):
        # tsm[0][task_id] = f"Generaing Audio {i+1} of {N}"

        await gen_and_save_audio(page['Script'], f'{AUDS_FOLDER}/{i}')


    tsm[0][task_id] = "Combining Images & video"
    print("\n", "combining audio and video")

    combine_audio_and_video(name)

    tsm[0][task_id] = "Uploading the video"
    print("\n", "uploading the video")
    
    upload_to_s3(name)
    
    ## updating quiz_data
    with open('quiz_data.json', 'r') as file:
        quiz_data = json.load(file)

    new_quiz_data = {
        "videoName": f"{file_path}.mp4",  
        "quiz": parsed_quiz_ans  
    }

    for video in quiz_data:
        if video["videoName"] == new_quiz_data["videoName"]:
            video["quiz"] = new_quiz_data["quiz"]  
            break
    else:
        quiz_data.append(new_quiz_data)

    with open('quiz_data.json', 'w') as file:
        json.dump(quiz_data, file, indent=2)
 
    tsm[0][task_id] = "Done"
    print("\n", "done!!!")
    
    END_TIME = time.time()
    print("Time taken: ", START_TIME-END_TIME)

    return


def upload_to_s3(name):
    s3 = boto3.client('s3')
    bucket_name = 'bajttv'
    file_path = f'vids/{name}.mp4'
    print(file_path)
    try:
        s3.upload_file(file_path, bucket_name, f'{name}.mp4')
        print("Upload successful!")
    except FileNotFoundError:
        print("The file was not found.")
    except NoCredentialsError:
        print("Credentials not available.")


def long_task(task_id: str, tsm: list):
    print(tsm[0])
    tsm[0][task_id] = "0% completed"  

    for i in range(1, 6):
        time.sleep(2)
        status = f"{i * 20}% completed"
        
        tsm[0][task_id] = status

    tsm[0][task_id] = "Done"