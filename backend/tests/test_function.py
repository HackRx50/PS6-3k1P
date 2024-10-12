import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
from pydub import AudioSegment

def combine_videos(video_folder, audio_folder, output_filename="combined_video_2.mp4", transition_duration=0.5):
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

    # Combine the video clips into one, with crossfade effect between them
    final_clip = concatenate_videoclips(clips, method="compose", padding=-transition_duration)
    
    # Get the duration of the combined video
    video_duration = final_clip.duration

    # Read the audio file
    audio_file = os.path.join(audio_folder, "happy-day-113985.mp3")
    if not os.path.isfile(audio_file):
        raise FileNotFoundError(f"The audio file {audio_file} was not found. Please check the path and ensure the file exists.")
    audio = AudioSegment.from_mp3(audio_file)

    # Adjust the audio duration to match the video duration
    if len(audio) / 1000 > video_duration:
        # If audio is longer, trim it
        audio = audio[:int(video_duration * 1000)]
    else:
        # If audio is shorter, loop it
        audio = audio * (int(video_duration * 1000 // len(audio)) + 1)
        audio = audio[:int(video_duration * 1000)]

    # Create a temporary directory for the adjusted audio
    temp_audio_dir = "temp_audio"
    os.makedirs(temp_audio_dir, exist_ok=True)
    temp_audio_path = os.path.join(temp_audio_dir, "adjusted_audio.mp3")

    # Export the adjusted audio
    audio.export(temp_audio_path, format="mp3")

    # Load the adjusted audio into the video
    video_with_audio = final_clip.set_audio(AudioFileClip(temp_audio_path))
    
    # Write the combined video with adjusted audio to a file
    video_with_audio.write_videofile(output_filename, codec="libx264", audio_codec="aac", threads=4, preset="ultrafast")

    # Close the clips to release memory
    for clip in clips:
        clip.close()
    final_clip.close()
    video_with_audio.close()

    # Remove the temporary audio file
    os.remove(temp_audio_path)
    os.rmdir(temp_audio_dir)

    print(f"Combined video with adjusted audio saved as {output_filename}")

# Example usage
combine_videos("stockvids/car", "audio")