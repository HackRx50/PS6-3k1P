import os
import json
import asyncio
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.functions import gen_and_save_audio

async def generate_audio_files(data):
    tasks = []
    for i, video_data in enumerate(data['videoData']):
        tasks.append(gen_and_save_audio(video_data['Subscript'], f'temp_auds/{i}', "english"))
    await asyncio.gather(*tasks)

async def combine_videos(video_folder, output_filename="combined_video_6.mp4", transition_duration=0.5):
    # Read the JSON data from testing.json
    with open('testing.json', 'r') as json_file:
        data = json.load(json_file)
    
    # Generate audio files concurrently
    await generate_audio_files(data)

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
            raise FileNotFoundError(f"The video file {video_file} was not found. Please check the path and ensure the file exists.")
    
    # Load all video clips and apply a crossfade transition to smooth out the transitions
    clips = [VideoFileClip(video_file) for video_file in video_files]

    # Apply crossfade to each clip to make the transitions smoother
    # Each video will fade in for the duration specified in `transition_duration`
    for i in range(1, len(clips)):
        clips[i] = clips[i].crossfadein(transition_duration)

    # Load audio files
    audio_files = [f'temp_auds/{i}_english.mp3' for i in range(len(data['videoData']))]
    audio_clips = [AudioFileClip(audio_file) for audio_file in audio_files]

    # Create a list to store video clips with their corresponding audio
    video_audio_clips = []

    # Combine each video clip with its corresponding audio
    for video_clip, audio_clip in zip(clips, audio_clips):
        video_with_audio = video_clip.set_audio(audio_clip)
        video_audio_clips.append(video_with_audio)

    # Combine the video clips into one, with crossfade effect between them
    final_clip = concatenate_videoclips(video_audio_clips, method="compose", padding=-transition_duration)

    # Write the combined video with synced audio to a file
    final_clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")

    # Close the clips to release memory
    for clip in clips:
        clip.close()
    for audio_clip in audio_clips:
        audio_clip.close()
    for video_audio_clip in video_audio_clips:
        video_audio_clip.close()
    final_clip.close()

    print(f"Combined video with sequentially synced audio saved as {output_filename}")

if __name__ == "__main__":
    asyncio.run(combine_videos("stockvids/car"))