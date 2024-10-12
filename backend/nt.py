from moviepy.editor import (AudioFileClip, CompositeAudioClip, VideoFileClip,
                            concatenate_audioclips, concatenate_videoclips)
import asyncio

from pdfminer.high_level import extract_text
from utils.new_funcs import *


async def main():
    processId = 'asdf'
    languages = ['english', 'hindi', 'marathi']
    captions = True
    # text = extract_text("uploads/private-car-package-policy.pdf")
    # scripts = await gen_script_and_choose_vid(text, 120)
    # print(scripts)

    scripts = [{'Subscript': "Owning a car is easier than ever, but maintaining it can be costly. That's where our comprehensive insurance comes in.", 'Video': 'vid2'}, {'Subscript': "Accidents happen. With our policy, you're covered for damages from theft, natural disasters, and even accidents.", 'Video': 'vid3'}, {'Subscript': "And it's not just your car. We protect your family too—you get liability coverage for injuries to third parties.", 'Video': 'vid4'}, {'Subscript': 'Introducing Bajaj Allianz Private Car Package Policy—designed to ensure that each drive comes with miles of smiles.', 'Video': 'vid1'},]
    for script in scripts:
      script['Script'] = script.pop('Subscript')
    # print(scripts)
    
    
    await gengen(scripts, processId, captions, languages)

    # await comb(vids, auds, f'{processId}')
    # add_subtitle(f"{processId}.mp4", "subtitles/4321.srt", f"{processId}_sub.mp4")

# Run the main function
asyncio.run(main())
