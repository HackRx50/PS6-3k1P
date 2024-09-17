import io
import os

import requests
from openai import OpenAI
from pdfminer.high_level import extract_text
from PIL import Image


def generate_image_from_text(prompt):
    prompt = prompt + " araminta_illus illustration style"
    api_url = "https://api-inference.huggingface.co/models/alvdansen/softserve_anime"  # anime
    # api_url = "https://api-inference.huggingface.co/modelsSebastianBodza/Flux_Aquarell_Watercolor_v2"

    headers = {"Authorization": "Bearer " + os.environ['FLUX_API_KEY']}
    data = {
        "inputs": prompt,
        "parameters": {
            "height": 200, "width": 400
        }
    }

    try:
        # Sending the request to Hugging Face API
        response = requests.post(
            api_url, headers=headers, json=data, timeout=300)

        # Handling successful request (status code 200)
        if response.status_code == 200:
            print("Image generation successful!")
            # Returning the image bytes
            return response.content
        else:
            # Handling the case of non-200 response
            print(f"Error: {response.status_code}, {response.text}")
            # Returning error message in bytes
            error_message = f"Error {response.status_code}: {response.text}"
            return error_message.encode('utf-8')  # Encoding error as bytes
    except Exception as e:
        # Handling any other unexpected errors (like network issues)
        print(f"An error occurred: {e}")
        # Return error message in bytes
        return f"An error occurred: {e}".encode('utf-8')


def create_video(file_path):
    print("creating video from the pdf", file_path)
    # get pdf content
    pdf_content = extract_text(file_path)

    print("hitting openai")
    # get openai slide breakdown
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": pdf_content + "\n\n" +
                "Break down the content into around 10 slides/pages and provide script for each slide. It must be in this format. Title: Introduction, Script: This is an introduction slide."},
        ]
    )
    ans = completion.choices[0].message.content

    slides = ans.split("---")

    # formatting the slides
    pgs = []
    for i in slides:
        i = i.strip("\n\n")
        if i.startswith("###"):
            pgs.append(i)
    slides = pgs

    # formatting the pages
    pages = []
    for slide in slides:
        page = {}
        sld = slide.split("### ")[1].split("\n")
        # page["title"] = sld[0]
        # page["title"]= sld[1].strip('**Title:**').strip()
        page["script"] = sld[1].strip('**Script:**').strip()
        # # page["image"]= sld[3].strip("**").strip('Image Prompt:**\n"')

        pages.append(page)

    print(pages)

    print("getting image prompts")
    # get image prompts for all scripts
    for i, page in enumerate(pages):
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user",
                    "content": "give just a short suitable prompt to give to an image generator as if talking to a 10 year old to create an image for the slide with this content: " + page["script"]}
            ]
        )
        ans = completion.choices[0].message.content
        page["image"] = ans

    print('clearing temp folders')
    IMGS_FOLDER = 'temp_imgs'
    AUDS_FOLDER = 'temp_auds'
    if os.path.exists(IMGS_FOLDER):
        os.rmdir(IMGS_FOLDER)
    if os.path.exists(AUDS_FOLDER):
        os.rmdir(AUDS_FOLDER)

    os.mkdir(IMGS_FOLDER)
    os.mkdir(AUDS_FOLDER)

    print("getting images")
    # creating images from prompts for all pages
    for i, page in enumerate(pages):
        print(page["image"])
        image_bytes = generate_image_from_text(page["image"])
        dataBytesIO = io.BytesIO(image_bytes)
        img = Image.open(dataBytesIO)
        img.save(f"{IMGS_FOLDER}/{i}.png")

    print("getting audios")
    # all audios from scripts
    for i,page in enumerate(pages):
        response = client.audio.speech.create(
          model="tts-1",
          voice="shimmer",
          input=page["script"]
        )

        with open(f'{AUDS_FOLDER}/{i}.mp3', 'wb') as f:
            f.write(response.content)

    return ans
