import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
from typing import List
import cloudinary
import cloudinary.uploader
import cloudinary.api
from typing import List

def combine_media(videos, audios, bg_music, captions, output):
    """
    Combines 4 videos, 4 audio tracks, background music, and captions into one final video.

    Parameters:
    videos (list): List of 4 video file paths.
    audios (list): List of 4 audio file paths.
    bg_music (str): Path to the background music file.
    captions (str): Path to the captions/subtitles file (e.g., .srt file).
    output (str): Path for the final output video.
    """
    
    if len(videos) != 4 or len(audios) != 4:
        raise ValueError("You must provide exactly 4 videos and 4 audios.")
    
    # FFmpeg command for concatenating the videos and mixing the audios
    command = [
        'ffmpeg',
        # Input videos
        '-i', videos[0], '-i', videos[1], '-i', videos[2], '-i', videos[3],
        # Input audios
        '-i', audios[0], '-i', audios[1], '-i', audios[2], '-i', audios[3],
        # Input background music
        '-i', bg_music,
        # FFmpeg filter complex to handle video concat, audio mix, and subtitles
        '-filter_complex', (
            '[0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0[v];'  # Concatenate videos
            '[4:a][5:a][6:a][7:a]amix=inputs=4:duration=longest[a_mix];'  # Mix audios
            '[a_mix][8:a]amix=inputs=2:duration=longest[a_final]'  # Add background music to the mix
        ),
        # Map the final video and audio streams
        '-map', '[v]',
        '-map', '[a_final]',
        # Include subtitles (captions) if provided
        # '-vf', f"subtitles={captions}",
        
        # Output file
        output
    ]
    
    # Run the command
    subprocess.run(command)

def combine_videos_and_audios(video_paths: List[str], audio_paths: List[str], output_path: str) -> None:
    # Load video clips
    video_clips = [VideoFileClip(path) for path in video_paths]
    
    # Concatenate video clips
    final_video = concatenate_videoclips(video_clips)
    
    # Load audio clips
    audio_clips = [AudioFileClip(path) for path in audio_paths]
    
    # Concatenate audio clips
    final_audio = concatenate_videoclips(audio_clips, method="compose")
    
    # Set the audio of the final video
    final_video = final_video.set_audio(final_audio)
    
    # Write the result to a file
    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
    # Close all clips to free up system resources
    final_video.close()
    for clip in video_clips + audio_clips:
        clip.close()

cloudinary.config(
    cloud_name = "dz1lxpkck",
    api_key = "895141239714285",
    api_secret = "3-z-J15QQQmB6EddTHws1-wzjF4"
)

def combine_videos_and_audios_cloudinary(video_public_ids: List[str], audio_public_ids: List[str], output_public_id: str) -> str:
    # Prepare the video concatenation
    video_parts = [{"public_id": vid} for vid in video_public_ids]
    
    # Prepare the audio concatenation
    audio_parts = [{"public_id": aud} for aud in audio_public_ids]
    
    # Combine videos
    video_upload_result = cloudinary.uploader.upload(
        "video:",
        public_id=f"{output_public_id}_video",
        resource_type="video",
        eager=[{
            "transformation": [
                {"overlay": vid, "width": 1920, "height": 1080, "crop": "scale"} 
                for vid in video_parts
            ],
            "format": "mp4"
        }],
        eager_async=True
    )
    
    # Combine audios
    audio_upload_result = cloudinary.uploader.upload(
        "video:",
        public_id=f"{output_public_id}_audio",
        resource_type="video",
        eager=[{
            "transformation": [
                {"overlay": aud} for aud in audio_parts
            ],
            "format": "mp3"
        }],
        eager_async=True
    )
    
    # Combine the concatenated video and audio
    final_upload_result = cloudinary.uploader.upload(
        f"video:cloudinary:{video_upload_result['public_id']}",
        public_id=output_public_id,
        resource_type="video",
        eager=[{
            "transformation": [
                {"overlay": f"video:{audio_upload_result['public_id']}", "flags": "layer_apply"}
            ],
            "format": "mp4"
        }],
        eager_async=True
    )
    
    # Return the URL of the resulting video
    return cloudinary.utils.cloudinary_url(output_public_id, resource_type="video", format="mp4")[0]


video_files = ['vid1.mp4', 'vid2.mp4', 'vid3.mp4', 'vid4.mp4']
audio_files = ['temp_audio_1_english.mp3', 'temp_audio_2_english.mp3', 'temp_audio_3_english.mp3', 'temp_audio_0_english.mp3']
captions_file = 'subtitles/4321.srt'
background_music = 'temp_audio/adjusted_background_audio.mp3'
output_file = 'output.mp4'

combine_videos_and_audios_cloudinary(video_files, audio_files, output_file)

# combine_videos_and_audios(video_files, audio_files, output_file)

