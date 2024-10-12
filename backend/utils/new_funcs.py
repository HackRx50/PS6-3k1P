from moviepy.editor import (AudioFileClip, CompositeAudioClip, VideoFileClip,
                            concatenate_audioclips, concatenate_videoclips)

from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
from google.oauth2 import service_account

from pydub import AudioSegment

import subprocess
from pydub.utils import mediainfo
import json
import asyncio
from openai import OpenAI

from database import *



def format_time(s):
    hours = int(s // 3600)
    minutes = int((s % 3600) // 60)
    seconds = int(s % 60)
    milliseconds = int((s - int(s)) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def get_audio_length(file_path):
    audio_info = mediainfo(file_path)
    return float(audio_info['duration'])

async def translate_text(text, target_language):

    credentials1 = service_account.Credentials.from_service_account_file(
        './service.json')

    translate_client = translate.Client(credentials=credentials1)

    # Translate the text into the target language
    result = translate_client.translate(text, target_language=target_language)
    translated_text = result["translatedText"]
    # print(f"Original Text: {text}")
    # print(f"Translated Text ({target_language}): {translated_text}")

    return translated_text

async def chat_completion(prompt):
    client = OpenAI()
    completion = await asyncio.to_thread(client.chat.completions.create,
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

async def classify_vid_genre(pdf_content):
    prompt = "Content: "+pdf_content+"\nClassify the above into one of three option based on what it is about.the options are Car, Health and Daily Needs.The output should be ONLY one of the options, nothing else"
    ans = await chat_completion(prompt)

    return ans

async def gen_script_and_choose_vid(pdf_content, n):

    description_dict = {
        "Car": {
            "vid1": "a man carefully takes care of his posh car by cleaning the window sill with his hands",
            "vid2": "BMW car driving down the road",
            "vid3": "a car accident with a truck in the highway",
            "vid4": "a happy family enjoying in their car"
        },
        "Health": {
            "vid1": "doctor treating a little girl, with mother by her side",
            "vid2": "people attending a funeral",
            "vid3": "cute baby playing with cake frosting in a lively family party",
            "vid4": "grandparents happily playing with grand children",
            "vid5": "surgeons treating a patient on an operation table",
            "vid6": "doctor discussing with family with patient in bed",
            "vid7": "analysing tax returns"
        },
        "Daily Needs": {
            "vid1": "a man is filling out bills",
            "vid2": "young boy gets injured and falls off the cycle, mother tends to him with a bandaid",
            "vid3": "a happy couple shops for groceries",
            "vid4": "working out in gym",
            "vid5": "heavy rains drowns a car"
        }
    }

    file_folder_dict = {
        "Car":"car",
        "Health":"hospital",
        "Daily Needs":"dailyNeeds"
    }
    
    chosen = await classify_vid_genre(pdf_content=pdf_content)
    print(chosen)
    
    desc_dict = json.dumps(description_dict[chosen])
    print(desc_dict)

    prompt = '''Think of yourself as an expert script writter for compeling social media video\n\nContent:''' + pdf_content + "\n\n" + \
        f'''From the content, make script for a concise and interesting video while keeping in mind that multiple corresponding videos will support each subscript.The description of the videos are as following. {desc_dict}. The script must have a storyline and be written keeping in mind the description of video. Do not use vid description to write the script, just use it to choose. The narrative should mention the product as the one that solves the problem. The entire script generated should be such that the time taken to speak collection of all subscripts is less than {n} seconds. Accordingly choose number of scripts. Format the answer only as a list of json objects with just 2 key called Subscript and Video. Only give the json. No emojis. '''

    ans = await chat_completion(prompt)
    print('asdf', ans)

    ans = ans.strip("```")
    ans = ans.split("json")[1]
    ans = ans.replace("\n", "")

    script_vid_slides = json.loads(ans)

    return script_vid_slides, file_folder_dict.get(chosen)

def gen_and_save_srt(scripts, name):
    print(scripts)
    cumulative_time_ms = 0
    srt_entry_number = 1
    srt_file_path = f'subtitles/{name}.srt'

    with open(srt_file_path, 'w', encoding="utf-8") as srt_file:
        for ind, script in enumerate(scripts):
            N = 3
            split = script.split(' ')
            split = [word for word in split if word.strip()]

            sentences = [' '.join(split[i:i+N])
                         for i in range(0, len(split), N)]
            # sentences = re.split(r'(?<=[,.])\s*', script)

            audio_length = get_audio_length(
                f'temp_auds/{name}_{ind}_english.mp3') * 1000

            total_script_length = len(script)

            for sentence in sentences:
                sentence_length = len(sentence)

                caption_duration_ms = (
                    sentence_length / total_script_length) * audio_length

                start_time_ms = cumulative_time_ms
                end_time_ms = start_time_ms + caption_duration_ms

                srt_entry = f"{srt_entry_number}\n{format_time(start_time_ms / 1000)} --> {format_time(end_time_ms / 1000)}\n{sentence}\n\n"
                srt_file.write(srt_entry)
                srt_entry_number += 1

                cumulative_time_ms += caption_duration_ms

async def gen_and_save_audio(script, file_path, language):

    if (language != "english"):
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

        translation_language_code = translation_language_codes.get(
            language.lower(), "hi")

        script = await translate_text(script, translation_language_code)

    credentials2 = service_account.Credentials.from_service_account_file(
        "./service2.json")

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

async def gengen(scripts, processId, chosen, languages):
    print('called', scripts)
    try:
        for script in scripts:
            script['Script'] = script.pop('Subscript')

        for i, language in enumerate(languages):
            for j, script in enumerate(scripts):
                await gen_and_save_audio(script['Script'], f'temp_auds/{processId}_{j}', language)

        vids = []
        scs = []
        for sc in scripts:
            vids.append(f"stockvids/{chosen}/{sc['Video']}.mp4")
            scs.append(sc['Script'])

        gen_and_save_srt(scs, processId)

        for lang in languages:
            audios = [f'temp_auds/{processId}_{i}_{lang}.mp3' for i in range(len(scripts))]

            await combcomb(vids, audios, f'vids/{processId}_{lang}_ttt')
            add_subtitle(f"vids/{processId}_{lang}_ttt.mp4", f"subtitles/{processId}.srt", f"vids/{processId}_{lang}.mp4")

    except Exception as e:
        print(e)
        return e

def audio_length(file_path):
    audio = AudioSegment.from_file(file_path)
    duration_in_milliseconds = len(audio)
    duration_in_seconds = duration_in_milliseconds / 1000
    return duration_in_seconds

async def combcomb(vids, auds, name):
    bajaj = "stockvids/bajaj/bajaj_logo.mp4"
    bg_aud = "temp_auds/bg_upbeat.mp3"
    
    audio_clips = [AudioFileClip(aud) for aud in auds]
    
    aud_lens = []
    for aud in auds:
        aud_lens.append(audio_length(aud))
    total_len = sum(aud_lens)

    clips = []
    for i,vid in enumerate(vids):
        clips.append(VideoFileClip(
            vid, target_resolution=(720, 1280), audio=False).subclip(0, aud_lens[i]))

    clip3 = VideoFileClip(bajaj, target_resolution=(720, 1280), audio=False)
    clips.append(clip3)

    # Combine the two video clips
    final_clip = concatenate_videoclips(clips)

    # Load the audio clips

    # Concatenate the audio clips
    audio = concatenate_audioclips(audio_clips)

    # Load the background audio
    bg_audio = AudioFileClip(bg_aud).subclip(0, total_len)

    audio = audio.volumex(0.8)  # Adjust volume of the main audio
    bg_audio = bg_audio.volumex(0.2)  # Adjust volume of the background audio

    # Combine the two audio clips
    combined_audio = CompositeAudioClip([audio, bg_audio])

    # Set the combined audio to the final video
    final_clip = final_clip.set_audio(combined_audio)

    # Write the result to a file (you can choose the output path and format)
    final_clip.write_videofile(
        f"{name}.mp4", codec="libx264", threads=8, preset='ultrafast')

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
