import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# Function to traverse directory and its subdirectories
def traverse_and_cut_videos(root_dir, output_dir, clip_duration=45):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith('.mp4'):
                full_path = os.path.join(dirpath, file)
                output_path = os.path.join(output_dir, os.path.splitext(file)[0] + '_clip.mp4')
                cut_video(full_path, output_path, clip_duration)

# Function to cut video into clips
def cut_video(video_path, output_path, clip_duration):
    # Get video duration using moviepy
    from moviepy.editor import VideoFileClip
    with VideoFileClip(video_path) as video:
        video_duration = video.duration
        num_clips = int(video_duration // clip_duration)
        
        for i in range(num_clips + 1):
            start_time = i * clip_duration
            end_time = min((i + 1) * clip_duration, video_duration)
            clip_output_path = output_path.replace('_clip.mp4', f'_clip_{i+1}.mp4')
            ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=clip_output_path)

if __name__ == "__main__":
    traverse_and_cut_videos("F:\\Stashed", "F:\\Clips")
