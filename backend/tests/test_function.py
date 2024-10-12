import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def combine_videos(video_folder, output_filename="combined_video.mp4", transition_duration=0.5):
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
            raise FileNotFoundError(f"The video file {video_file} was not found. Please check the path: {video_file}")
    
    # Load all video clips and apply a crossfade transition to smooth out the transitions
    clips = [VideoFileClip(video_file) for video_file in video_files]

    # Apply crossfade to each clip to make the transitions smoother
    # Each video will fade in for the duration specified in `transition_duration`
    for i in range(1, len(clips)):
        clips[i] = clips[i].crossfadein(transition_duration)

    # Combine the video clips into one, with crossfade effect between them
    final_clip = concatenate_videoclips(clips, method="compose", padding=-transition_duration)
    
    # Write the combined video to a file
    final_clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")

    # Close the clips to release memory
    for clip in clips:
        clip.close()

    print(f"Combined video saved as {output_filename}")

# Example usage
combine_videos(r"C:\Projects\hackrx\backend\stockvids\car")
