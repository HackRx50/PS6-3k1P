from utils.functions import *
import asyncio

# Paths to your video and audio files
vids = ["stockvids/car/vid1.mp4", "stockvids/car/vid2.mp4"]
bajaj = "stockvids/bajaj/bajaj_logo.mp4"
auds = ["temp_audio/temp_audio_0_english.mp3", "temp_audio/temp_audio_1_english.mp3"]
bg_aud = "temp_audio/adjusted_background_audio.mp3"

from moviepy.editor import VideoFileClip, concatenate_videoclips, concatenate_audioclips, AudioFileClip, CompositeAudioClip
# Load the video clips

async def comb(vids, auds, name):
  clips = []
  for vid in vids:
    clips.append(VideoFileClip(vid, target_resolution=(720, 1280), audio=False))
  
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
  final_clip.write_videofile(f"{name}.mp4", codec="libx264", threads=8, preset='ultrafast')



async def main():
  processId = 'asdf'
  await comb(vids, auds, f'{processId}')
  add_subtitle(f"{processId}.mp4", "subtitles/4321.srt", f"{processId}_sub.mp4")

# Run the main function
asyncio.run(main())