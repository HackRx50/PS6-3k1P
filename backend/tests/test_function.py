import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip, concatenate_audioclips
from pydub import AudioSegment

def combine_videos(video_folder, audio_folder, output_filename="combined_video_with_speech_and_music.mp4", transition_duration=0.5):
    # Get the paths of the video and audio speech files
    video_files = [
        os.path.join(video_folder, "vid1.mp4"),
        os.path.join(video_folder, "vid2.mp4"),
        os.path.join(video_folder, "vid3.mp4"),
        os.path.join(video_folder, "vid4.mp4")
    ]
    
    speech_files = [
        os.path.join("temp_audio", "aud_1.mp3"),
        os.path.join("temp_audio", "aud_2.mp3"),
        os.path.join("temp_audio", "aud_3.mp3"),
        os.path.join("temp_audio", "aud_4.mp3")
    ]
    
    # Ensure all video and speech files exist
    for video_file, speech_file in zip(video_files, speech_files):
        if not os.path.isfile(video_file):
            raise FileNotFoundError(f"The video file {video_file} was not found. Please check the path and ensure the file exists.")
        if not os.path.isfile(speech_file):
            raise FileNotFoundError(f"The audio file {speech_file} was not found. Please check the path and ensure the file exists.")
    
    # Load all video clips
    video_clips = [VideoFileClip(video_file) for video_file in video_files]
    
    # Load all audio speech clips
    speech_audio_clips = [AudioFileClip(speech_file) for speech_file in speech_files]
    
    # Adjust video duration to match the audio speech duration by cropping
    cropped_video_clips = []
    for video_clip, speech_audio_clip in zip(video_clips, speech_audio_clips):
        video_duration = video_clip.duration
        audio_duration = speech_audio_clip.duration
        
        # Crop video to match the length of the corresponding audio
        if video_duration > audio_duration:
            cropped_video = video_clip.subclip(0, audio_duration)  # Trim video to match audio duration
        else:
            cropped_video = video_clip  # No need to trim if the video is shorter or equal to the audio
        
        cropped_video_clips.append(cropped_video)
    
    # Apply crossfade transition between video clips
    for i in range(1, len(cropped_video_clips)):
        cropped_video_clips[i] = cropped_video_clips[i].crossfadein(transition_duration)
    
    # Combine the video clips into one
    final_clip = concatenate_videoclips(cropped_video_clips, method="compose", padding=-transition_duration)
    
    # Get the duration of the combined video
    video_duration = final_clip.duration

    # Read the background music file
    music_file = os.path.join(audio_folder, "happy-day-113985.mp3")
    if not os.path.isfile(music_file):
        raise FileNotFoundError(f"The music file {music_file} was not found. Please check the path and ensure the file exists.")
    
    # Load the background music
    background_music_clip = AudioFileClip(music_file)

    # Reduce the volume of the background music
    background_music_clip = background_music_clip.volumex(0.1)  # Adjust the factor as needed

    # Combine the speech audio with the background music
    combined_audio_clips = []
    current_time = 0
    for speech_clip in speech_audio_clips:
        combined_audio = CompositeAudioClip([
            speech_clip,
            background_music_clip.subclip(current_time, current_time + speech_clip.duration)
        ])
        combined_audio_clips.append(combined_audio)
        current_time += speech_clip.duration

    # Concatenate the combined audio clips
    final_audio = concatenate_audioclips(combined_audio_clips)

    # Set the combined audio to the final video clip
    final_clip = final_clip.set_audio(final_audio)
    
    # Write the final video to a file
    final_clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")
    
    # Close clips to free memory
    for clip in video_clips:
        clip.close()
    for speech_clip in speech_audio_clips:
        speech_clip.close()
    background_music_clip.close()
    final_clip.close()

    print(f"Combined video with speech and background music saved as {output_filename}")

# Example usage with correct folder structure
combine_videos(
    video_folder="stockvids/car",
    audio_folder="audio_music"
)
