import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

def combine_videos(video_folder, audio_folder, output_filename="combined_video_with_speech.mp4", transition_duration=0.5):
    # Get the paths of the video and audio speech files
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
        
        # Set the corresponding audio to the video
        video_with_audio = cropped_video.set_audio(speech_audio_clip)
        cropped_video_clips.append(video_with_audio)
    
    # Apply crossfade transition between video clips
    for i in range(1, len(cropped_video_clips)):
        cropped_video_clips[i] = cropped_video_clips[i].crossfadein(transition_duration)
    
    # Combine the video clips into one
    final_clip = concatenate_videoclips(cropped_video_clips, method="compose", padding=-transition_duration)
    
    # Write the final video to a file
    final_clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")
    
    # Close clips to free memory
    for clip in video_clips:
        clip.close()
    for speech_clip in speech_audio_clips:
        speech_clip.close()
    final_clip.close()

    print(f"Combined video with speech saved as {output_filename}")

# Example usage with your specified paths
combine_videos(
    video_folder=r"C:\Projects\hackrx\backend\stockvids\car",
    audio_folder=r"C:\Projects\hackrx\backend\temp_audio"
)
