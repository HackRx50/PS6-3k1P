import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip, concatenate_audioclips
from pydub import AudioSegment

def combine_videos(video_folder, audio_folder, output_filename="combined_video_with_speech_and_music.mp4", transition_duration=0.5):
    # Get the paths of the video and audio files
    video_files = [
        os.path.join(video_folder, "vid1.mp4"),
        os.path.join(video_folder, "vid2.mp4"),
        os.path.join(video_folder, "vid3.mp4"),
        os.path.join(video_folder, "vid4.mp4")
    ]
    
    speech_files = [
        os.path.join(audio_folder, "aud1.mp3"),
        os.path.join(audio_folder, "aud2.mp3"),
        os.path.join(audio_folder, "aud3.mp3"),
        os.path.join(audio_folder, "aud4.mp3")
    ]
    
    # Ensure all video and speech files exist
    for video_file, speech_file in zip(video_files, speech_files):
        if not os.path.isfile(video_file):
            raise FileNotFoundError(f"The video file {video_file} was not found.")
        if not os.path.isfile(speech_file):
            raise FileNotFoundError(f"The audio file {speech_file} was not found.")
    
    # Load all video clips and apply crossfade
    clips = [VideoFileClip(video_file) for video_file in video_files]
    
    # Apply crossfade transition between clips
    for i in range(1, len(clips)):
        clips[i] = clips[i].crossfadein(transition_duration)

    # Combine the video clips into one
    final_clip = concatenate_videoclips(clips, method="compose", padding=-transition_duration)
    
    # Combine speech audio with video
    speech_audio_clips = [AudioFileClip(speech_file) for speech_file in speech_files]

    # Concatenate all the speech audio clips
    final_speech_audio = concatenate_audioclips(speech_audio_clips)
    
    # Get the duration of the combined video
    video_duration = final_clip.duration
    
    # Load and adjust background music
    background_music_file = os.path.join(audio_folder, "happy-day-113985.mp3")
    if not os.path.isfile(background_music_file):
        raise FileNotFoundError(f"The background music file {background_music_file} was not found.")
    
    background_music = AudioSegment.from_mp3(background_music_file)
    
    # Adjust the background music to match the duration of the final video
    if len(background_music) / 1000 > video_duration:
        background_music = background_music[:int(video_duration * 1000)]
    else:
        background_music = background_music * (int(video_duration * 1000 // len(background_music)) + 1)
        background_music = background_music[:int(video_duration * 1000)]
    
    # Create a temporary directory for the adjusted background music
    temp_audio_dir = "temp_audio"
    os.makedirs(temp_audio_dir, exist_ok=True)
    temp_background_music_path = os.path.join(temp_audio_dir, "adjusted_background_music.mp3")
    
    # Export the adjusted background music
    background_music.export(temp_background_music_path, format="mp3")
    
    # Load the background music as an AudioFileClip
    background_music_clip = AudioFileClip(temp_background_music_path)
    
    # Combine the final speech audio with the background music using CompositeAudioClip
    final_audio = CompositeAudioClip([final_speech_audio, background_music_clip.set_duration(video_duration)])
    
    # Set the audio of the final video to the combined speech and background music
    final_video_with_audio = final_clip.set_audio(final_audio)
    
    # Write the final video with audio to the output file
    final_video_with_audio.write_videofile(output_filename, codec="libx264", audio_codec="aac")
    
    # Close clips to free memory
    for clip in clips:
        clip.close()
    final_clip.close()
    final_video_with_audio.close()
    
    # Remove temporary files
    os.remove(temp_background_music_path)
    os.rmdir(temp_audio_dir)
    
    print(f"Combined video with speech and background music saved as {output_filename}")

# Example usage with your specified paths
combine_videos(
    video_folder=r"C:\Projects\hackrx\backend\stockvids\car",
    audio_folder=r"C:\Projects\hackrx\backend\temp_audio"
)
