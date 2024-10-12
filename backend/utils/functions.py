import asyncio
import io
import json
import os
import re
import subprocess
import time

import boto3
import requests
from botocore.client import Config
from database import *
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips
from openai import OpenAI
from pdfminer.high_level import extract_text
from PIL import Image
from pydub.utils import mediainfo
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
from google.oauth2 import service_account

IMGS_FOLDER = 'temp_imgs'
AUDS_FOLDER = 'temp_auds'

def stock_videos(video_folder, output_filename="combined_video.mp4", transition_duration=0.5):
    # Get the paths of the video files
    video_files = [
        os.path.join(video_folder, "vid1.mp4"),
        os.path.join(video_folder, "vid2.mp4"),
        os.path.join(video_folder, "vid3.mp4"),
        os.path.join(video_folder, "vid4.mp4")
    ]
    
    # Ensure all video files exist
    for video_file in video_files:
        if not os.path.isfile(video_file):
            raise FileNotFoundError(f"The video file {video_file} was not found. Please check the path: {video_file}")
    
    # Load all video clips and apply a crossfade transition to smooth out the transitions
    clips = [VideoFileClip(video_file) for video_file in video_files]

    # Apply crossfade to each clip to make the transitions smoother
    # Each video will fade in for the duration specified in `transition_duration`
    for i in range(1, len(clips)):
        clips[i] = clips[i].crossfadein(transition_duration)

    # Combine the video clips into one, with crossfade effect between them
    final_clip = concatenate_videoclips(clips, method="compose", padding=-transition_duration)
    
    # Write the combined video to a file
    final_clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")

    # Close the clips to release memory
    for clip in clips:
        clip.close()

    print(f"Combined video saved as {output_filename}")

async def gen_and_save_image(prompt, file_path, height, width):
    image_bytes = await generate_image_from_text(prompt, height, width)
    dataBytesIO = io.BytesIO(image_bytes)
    img = Image.open(dataBytesIO)
    
    print("Saving image", file_path)
    folder = os.path.dirname(file_path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    img.save(f"{file_path}.png")

async def translate_text(text, target_language):

    credentials1 = service_account.Credentials.from_service_account_file('./service.json')

    translate_client = translate.Client(credentials=credentials1)

    # Translate the text into the target language
    result = translate_client.translate(text, target_language=target_language)
    translated_text = result["translatedText"]
    # print(f"Original Text: {text}")
    # print(f"Translated Text ({target_language}): {translated_text}")

    return translated_text

async def gen_and_save_audio(script, file_path, language):

    if(language!="english"):
        translation_language_codes = {
            "hindi": "hi",
            "marathi": "mr",
            "tamil": "ta",
            "telugu": "te",
            "malayalam": "ml",
            "kannada": "kn",
            "bengali": "bn",
            "punjabi": "pa",
        }

        translation_language_code = translation_language_codes.get(language.lower(), "hi")

        script = await translate_text(script, translation_language_code)

    credentials2 = service_account.Credentials.from_service_account_file("./service2.json")
    
    # Initialize the Text-to-Speech client with credentials
    client = texttospeech.TextToSpeechClient(credentials=credentials2)

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=script)

    language_codes = {
        "english": "en-US",
        "hindi": "hi-IN",
        "marathi": "mr-IN",
        "tamil": "ta-IN",
        "telugu": "te-IN",
        "malayalam": "ml-IN",
        "kannada": "kn-IN",
        "bengali": "bn-IN",
        "punjabi": "pa-IN",
    }

    # Get the language code from the dictionary
    tts_language_code = language_codes.get(language.lower(), "en-IN")


    # Build the voice request, select the language code and voice
    voice = texttospeech.VoiceSelectionParams(
        language_code=tts_language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the audio configuration
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # client = OpenAI()
    # # Run the synchronous call in a separate thread
    # response = await asyncio.to_thread(client.audio.speech.create,
    #     model="tts-1",
    #     voice="shimmer",
    #     input=script
    # )

    with open(f'./{file_path}_{language}.mp3', 'wb') as f:
        f.write(response.audio_content)

async def gen_and_save_quiz(script_compiled, name):
    ## Create quiz 
    print("\n", "Generating and Saving Quiz")
    
    prompt = "Generate 10 simple quiz questions with 4 options to choose from, using the content of the script. Keep the questions things that customer should know about Bajaj Allianz. Script:"+ script_compiled + ". It must be in json format with 3 keys: question, options(4) and correctAnswer. Don't answer anything other than the json"

    quiz_ans = await chat_completion(prompt)

    quiz_ans = quiz_ans.strip("```")
    quiz_ans = quiz_ans.split("json")[1]
    quiz_ans = quiz_ans.replace("\n", "")

    parsed_quiz_data = json.loads(quiz_ans)
    print("pp", parsed_quiz_data)
    
    await upload_quiz_data(parsed_quiz_data, name)

async def generate_image_from_text(prompt, height, width):
    
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
    # API_URL = "https://api-inference.huggingface.co/models/alvdansen/softserve_anime"  # anime
    # API_URL = "https://api-inference.huggingface.co/modelsSebastianBodza/Flux_Aquarell_Watercolor_v2"

    headers = {"Authorization": "Bearer " + os.environ['FLUX_API_KEY']}
    data = {
        "inputs": "Ultra realistic. " + prompt,
        "parameters": {
            "height": height, "width": width
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=300)

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

async def chat_completion(prompt):
    client = OpenAI()
    completion = await asyncio.to_thread(client.chat.completions.create,
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

async def generate_image(script, ind, processId, height, width):
    try:
        # prompt = "give just a short suitable prompt to give to an image generator as if talking to a 10 year old to create an image for the slide with this content: " + script
        prompt = "give the shortest prompt to give to an image generator to generate a stock image for this content: " + script
        imp = await chat_completion(prompt)
        img_prompt = imp.strip('"')

        print("img_prompt", img_prompt)
        
        img_path = f"temp_imgs/{processId}/{ind}"
        await gen_and_save_image(img_prompt, img_path, height, width)
        return
    except Exception as e:
        print(e)
        return e

async def generate_video(scripts, processId, captions, languages):
    try:
        translation_language_codes = {
            "hindi": "hi",
            "marathi": "mr",
            "tamil": "ta",
            "telugu": "te",
            "malayalam": "ml",
            "kannada": "kn",
            "bengali": "bn",
            "punjabi": "pa",
        }
        
        # for i, language in enumerate(languages):
        #     for j, script in enumerate(scripts):
        #         await gen_and_save_audio(script['Script'], f'temp_auds/{processId}_{j}', language)
        
        lang = 'marathi'

        translation_language_code = translation_language_codes.get(lang.lower(), "hi")

        lang_scripts = []
        for script in scripts:
            translated_script = await translate_text(script['Script'], translation_language_code)
            lang_scripts.append(translated_script)
        gen_and_save_srt(lang_scripts, f'{processId}_{lang}')
        
        # audios = [f'temp_auds/{processId}_{i}_{lang}.mp3' for i in range(len(scripts))]
        # images = sorted([f"temp_imgs/{processId}/{f}" for f in os.listdir(f"temp_imgs/{processId}") if f.endswith('.png')])
        
        # print("audios", audios)
        # print("images", images)
        
        
        # # combine audio and video.
        # await combine_audio_and_video(f'{processId}_{lang}', audios, images)
        # add_subtitle(f'vids/{processId}_{lang}.mp4', f'subtitles/{processId}.srt', f'vids/{processId}_{lang}_final.mp4')
        
    except Exception as e:
        print(e)
        return e

async def get_script_from_pdf(file_path, n):
    pdf_content = extract_text(file_path)
    pages = await get_main_content(pdf_content, n)
    return pages

async def get_main_content(pdf_content, n):
    
    prompt = pdf_content + "\n\n" + f"Break down the content into {n} slides/pages and provide script for each slide. It must be a json list of objects with just 2 keys, Script and Title, nothing else"

    ans = await chat_completion(prompt)
    
    ans = ans.strip("```")
    ans = ans.split("json")[1]
    ans = ans.replace("\n", "")

    parsed_slides = json.loads(ans)
    print("parsed_slides", parsed_slides)

    return parsed_slides

async def create_video(file_path: str, task_id: str, tsm: list):
    START_TIME = time.time()
    
    name = os.path.basename(file_path).split(".")[0]
    
    print("\n", "creating video from the pdf", file_path)
    pdf_content = extract_text(file_path)

    tsm[0][task_id] = "Generating Script"
    print("\n", "Generating Script")
    pages = await get_main_content(pdf_content, 10)

    print("\n", "pages", pages)
    
    async def add_image_prompt(i):
        print(f"getting prompt for image {i}")
        prompt = "give just a short suitable prompt to give to an image generator as if talking to a 10 year old to create an image for the slide with this content: " + pages[i]["Script"]
        imp = await chat_completion(prompt)
        pages[i]['image'] = imp.strip('"')

    script_compiled=""
    CompletionTasks = []
    for i in range(len(pages)):
        CompletionTasks.append(add_image_prompt(i))
        script_compiled=script_compiled + pages[i]["Script"]

    tsm[0][task_id] = "Image Prompts"
    print("\n", "Image Prompts")
    await asyncio.gather(*CompletionTasks)
    
    tsm[0][task_id] = "Generating Quiz"
    print("\n", "Generating Quiz")
    await gen_and_save_quiz(script_compiled, name)

    print('\n', "clearing temp folders")
    await clear_temp_folders()

    PostScriptTasks = []  
    for i, page in enumerate(pages):
        try:
            PostScriptTasks.append(gen_and_save_image(page["image"], f"{IMGS_FOLDER}/{i}")) # image
            PostScriptTasks.append(gen_and_save_audio(page['Script'], f'{AUDS_FOLDER}/{i}',"english"))# audio
        except Exception as e:
            print(e)
            return e

    tsm[0][task_id] = "Generating Images and Audios"
    print("\n", "Generating Images and Audios")
    await asyncio.gather(*PostScriptTasks)

    tsm[0][task_id] = "Combining Images & video"
    print("\n", "combining audio and video")
    await combine_audio_and_video(name+"_t")
    
    gen_and_save_srt(pages, name)
    add_subtitle(f'vids/{name}_t.mp4', f'tmp/{name}.srt', f'vids/{name}.mp4')

    tsm[0][task_id] = "Uploading the video"
    print("\n", "uploading the video")
    await upload_to_s3(name)

    tsm[0][task_id] = "Done"
    print("\n", "done!!!")

    END_TIME = time.time()
    print("Time taken: ", END_TIME-START_TIME)

    return

async def upload_to_s3(name):
    # s3 = boto3.client('s3')
    s3 = boto3.client('s3', region_name="ap-south-1", config=Config(signature_version='s3v4'))
    bucket_name = 'bajttv'
    file_path = f'vids/{name}'
    print(file_path)
    try:
        s3.upload_file(file_path, bucket_name, f'{name}.mp4')
        print("Upload successful!")
    except FileNotFoundError:
        print("The file was not found.")

async def upload_quiz_data(parsed_quiz_data, name):
    full_name = f"{name}.mp4"

    try:
        db = next(get_db())  # Get a database session
        existing_quiz = db.query(QuizDataDB).filter(QuizDataDB.video_name == full_name).first()

        if existing_quiz:
            return
        else:
            # Create a new record
            for qns in parsed_quiz_data:
                print(qns)
                quiz_data_entry = QuizDataDB(
                    video_name=full_name,
                    question=qns['question'],  # Store as JSON string
                    options=json.dumps(qns['options']),  # Placeholder for options
                    correct_answer=qns['correctAnswer']  # Placeholder for correct answer
                )
                db.add(quiz_data_entry)
        db.commit()  # Save changes
        db.close()  # Close the session
    except Exception as e:
        print(f"An error occurred: {e}")

async def combine_audio_and_video(name, audio_files, image_files):

    video_clips = []

    for i, audio_file in enumerate(audio_files):
        
        audio_clip = AudioFileClip(audio_file)
        
        image_clip = ImageClip(image_files[i]).set_duration(audio_clip.duration)
        
        video_clip = image_clip.set_audio(audio_clip)
        
        video_clips.append(video_clip)

    final_video = concatenate_videoclips(video_clips)

    output_path = 'vids/' + name + '.mp4'
    final_video.write_videofile(output_path, fps=24)

    print("Video created successfully!")

def add_subtitle(input_file, subtitle_file, output_file):
    # FFmpeg command to add subtitles to the input video
    ffmpeg_command = [
        "ffmpeg",
        "-y",                            # Overwrite output files without asking
        "-i", input_file,                # Input video file
        "-vf", f"subtitles={subtitle_file}",  # Add subtitles from the SRT file
        "-c:v", "libx264",               # Video codec (H.264)
        "-c:a", "copy",                  # Copy audio without re-encoding
        output_file
    ]

    # Run the FFmpeg command
    subprocess.run(ffmpeg_command)

async def clear_temp_folders():
    if os.path.exists(IMGS_FOLDER):
        for file in os.listdir(IMGS_FOLDER):
            os.remove(os.path.join(IMGS_FOLDER, file))
    else:
        os. makedirs(IMGS_FOLDER)

    if os.path.exists(AUDS_FOLDER):
        for file in os.listdir(AUDS_FOLDER):
            os.remove(os.path.join(AUDS_FOLDER, file))
    else:
        os.makedirs(AUDS_FOLDER)
    print('done')
    return

def prepare_folders():
    UPLOAD_FOLDER = 'uploads'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    VIDEO_FOLDER = 'vids'
    if not os.path.exists(VIDEO_FOLDER):
        os.makedirs(VIDEO_FOLDER)

def format_time(s):
    hours = int(s // 3600)
    minutes = int((s % 3600) // 60)
    seconds = int(s % 60)
    milliseconds = int((s - int(s)) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def get_audio_length(file_path):
    audio_info = mediainfo(file_path)
    return float(audio_info['duration'])

def gen_and_save_srt(scripts, name):
    cumulative_time_ms = 0  
    srt_entry_number = 1  
    srt_file_path = f'subtitles/{name}.srt'  

    
    with open(srt_file_path, 'w', encoding="utf-8") as srt_file:
        for ind, script in enumerate(scripts):
            
            N = 3
            split = script.split(' ')
            split = [word for word in split if word.strip()]

            sentences = [' '.join(split[i:i+N]) for i in range(0, len(split), N)]            
            # sentences = re.split(r'(?<=[,.])\s*', script)
            print(sentences)
            
            audio_length = get_audio_length(f'temp_auds/{name}_{ind}_English.mp3') * 1000  
            
            total_script_length = len(script)  
            
            for sentence in sentences:
                sentence_length = len(sentence)  
                
                caption_duration_ms = (sentence_length / total_script_length) * audio_length
                
                start_time_ms = cumulative_time_ms
                end_time_ms = start_time_ms + caption_duration_ms
                
                srt_entry = f"{srt_entry_number}\n{format_time(start_time_ms / 1000)} --> {format_time(end_time_ms / 1000)}\n{sentence}\n\n"
                srt_file.write(srt_entry)  
                srt_entry_number += 1  
                
                cumulative_time_ms += caption_duration_ms
