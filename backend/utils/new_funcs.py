
from pydub.utils import mediainfo
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
from google.oauth2 import service_account


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

async def gen_script_and_choose_vid(pdf_content, n):

    description_dict = {
        "Car": "vid1 description: a man carefully takes care of his posh car by cleaning the window sill with his hands. vid2 description: BMW car driving down the road. vid3 description: a car accident with a truck in the highway. vid4 description: a happy family enjoying in their car.",
        "Health": "vid1 description: doctor treating a little girl, with mother by her side. vid2 description: people attending a funeral. vid3 description: cute baby playing with cake frosting in a lively family party. vid4 description: grandparents happily playing with grand children. vid5 description: surgeons treating a patient on an operation table. vid6 description: doctor discussing with family with patient in bed. vid7 description: analysing tax returns",
        "Daily Needs": "vid1 description: a man is filling out bills. vid2 description: young boy gets injured and falls off the cycle, mother tends to him with a bandaid. vid3 description: a happy couple shops for groceries. vid4 description: working out in gym. vid5 description: heavy rains drowns a car"
    }

    chosen = await classify_vid_genre(pdf_content=pdf_content)
    print(chosen)

    chosen_description = description_dict.get(chosen)

    prompt = '''Think of yourself as an expert script writter for compeling social media video\n\nContent:''' + pdf_content + "\n\n" + \
        f'''From the content,make script for a concise and interesting video while keeping in mind that multiple corresponding videos will support each subscript.The description of the videos are as following. {chosen_description} The script must have a storyline and be written keeping in mind the description of video. Do not use vid description to write the script, just use it to choose. The narrative should mention the product as the one that solves the problem. The entire script generated should be such that the time taken to speak collection of all subscripts is less than {n} seconds. Accordingly choose number of scripts. Use simpler language, make it sound more natural like someone is narrating a story. The time taken to speak each subscript should be less than 10 seconds.  The subscripts must collectively include all the important information in content for any customer. The answer should contain the subscript to be spoken and corresponding vid. Format the answer only as a list of json objects with just 2 key called Subscript and Video. Only give the json. No emojis. '''

    ans = await chat_completion(prompt)
    ans = ans.strip("```")
    ans = ans.split("json")[1]
    ans = ans.replace("\n", "")

    script_vid_slides = json.loads(ans)

    return script_vid_slides

def gen_and_save_srt(scripts, name):
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
            print(sentences)

            audio_length = get_audio_length(
                f'temp_auds/{name}_{ind}_English.mp3') * 1000

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

async def gengen(scripts, processId, captions, languages):
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

        lang = 'english'

        translation_language_code = translation_language_codes.get(
            lang.lower(), "hi")

        lang_scripts = []
        for script in scripts:
            translated_script = await translate_text(script['Script'], translation_language_code)
            lang_scripts.append(translated_script)
        gen_and_save_srt(lang_scripts, f'{processId}_{lang}')

        vids = []
        for sc in scripts:
            vids.append(f"stockvids/car/{sc['Video']}.mp4")
        print(vids)

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

async def combcomb(vids, auds, name):
    clips = []
    for vid in vids:
        clips.append(VideoFileClip(
            vid, target_resolution=(720, 1280), audio=False))

    clip3 = VideoFileClip(bajaj, target_resolution=(720, 1280), audio=False)
    clips.append(clip3)

    # Combine the two video clips
    final_clip = concatenate_videoclips(clips)

    # Load the audio clips
    audio_clips = [AudioFileClip(aud) for aud in auds]

    # Concatenate the audio clips
    audio = concatenate_audioclips(audio_clips)

    # Load the background audio
    bg_audio = AudioFileClip(bg_aud)

    audio = audio.volumex(0.8)  # Adjust volume of the main audio
    bg_audio = bg_audio.volumex(0.2)  # Adjust volume of the background audio

    # Combine the two audio clips
    combined_audio = CompositeAudioClip([audio, bg_audio])

    # Set the combined audio to the final video
    final_clip = final_clip.set_audio(combined_audio)

    # Write the result to a file (you can choose the output path and format)
    final_clip.write_videofile(
        f"{name}.mp4", codec="libx264", threads=8, preset='ultrafast')

