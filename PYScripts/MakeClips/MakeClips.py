import os
import subprocess
import re
from datetime import timedelta

# --- Configuration ---
# Set the full path to the ffmpeg/ffprobe executable.
# It is critical that this path is correct.
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
FFPROBE_PATH = r"C:\ffmpeg\bin\ffprobe.exe"

# Set the source directory to search for MP4 files.
SOURCE_DIR = r"F:\Stashed"

# Set the destination directory for the output sample videos.
OUTPUT_DIR = r"F:\Temp"

# --- Main Script ---

def get_video_duration(video_path):
    """
    Uses ffprobe to get the duration of a video file in seconds.
    
    Args:
        video_path (str): The full path to the video file.

    Returns:
        float: The duration of the video in seconds, or None if an error occurs.
    """
    try:
        # Construct the ffprobe command to get the duration.
        # -v error: Suppress all output except for errors.
        # -show_entries format=duration: Show only the duration field.
        # -of default=noprint_wrappers=1: No extra text, just the duration value.
        cmd = [
            FFPROBE_PATH,
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        
        # Run the command and capture the output.
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # The output is a string of the duration. Convert to float.
        duration_str = result.stdout.strip()
        if duration_str:
            return float(duration_str)
        else:
            print(f"Warning: Could not get duration for '{video_path}'. Output was empty.")
            return None

    except subprocess.CalledProcessError as e:
        print(f"Error calling ffprobe on '{video_path}': {e}")
        return None
    except FileNotFoundError:
        print(f"Error: ffprobe not found at '{FFPROBE_PATH}'. Please check the path.")
        return None
    except ValueError:
        print(f"Error: Could not parse duration from ffprobe output for '{video_path}'.")
        return None


def create_video_sample(input_path, output_path, start_time_seconds, duration_seconds=10):
    """
    Uses ffmpeg to create a 10-second sample from a video.
    
    Args:
        input_path (str): The full path to the source video file.
        output_path (str): The full path for the output sample file.
        start_time_seconds (float): The start time of the sample in seconds.
        duration_seconds (int): The duration of the sample clip in seconds.
    """
    try:
        # Use timedelta to format the start time for ffmpeg in HH:MM:SS.ss format.
        start_time_formatted = str(timedelta(seconds=start_time_seconds))

        # The ffmpeg command:
        # -ss {start_time}: Specifies the start time of the clip.
        # -i {input_path}: Specifies the input file.
        # -t {duration}: Specifies the duration of the clip.
        # -c copy: Copies the video and audio streams without re-encoding, which is very fast.
        cmd = [
            FFMPEG_PATH,
            "-ss", start_time_formatted,
            "-i", input_path,
            "-t", str(duration_seconds),
            "-c", "copy",
            output_path
        ]
        
        # Run the command. The check=True argument will raise an exception if the command fails.
        subprocess.run(cmd, check=True)
        print(f"Successfully created sample: {output_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error creating sample for '{input_path}': {e}")
    except FileNotFoundError:
        print(f"Error: ffmpeg not found at '{FFMPEG_PATH}'. Please check the path.")


def main():
    """
    The main function to orchestrate the video sampling process.
    """
    if not os.path.isdir(SOURCE_DIR):
        print(f"Error: Source directory not found at '{SOURCE_DIR}'.")
        return

    if not os.path.isdir(OUTPUT_DIR):
        print(f"Output directory not found at '{OUTPUT_DIR}'. Creating it now.")
        os.makedirs(OUTPUT_DIR)

    # --- Temporary limit for testing ---
    # Set a limit to process only the first 5 files.
    # To process all files, simply comment out the next two lines.
    file_limit = 5
    file_count = 0

    # Use os.walk to traverse the source directory and its subdirectories.
    for root, _, files in os.walk(SOURCE_DIR):
        for filename in files:
            # Check if the file is an MP4 video.
            if filename.lower().endswith(".mp4"):
                # Check the file count. If the limit is reached, exit the script.
                if file_count >= file_limit:
                    print(f"\nFile limit of {file_limit} reached. Stopping now.")
                    return

                # Increment the counter for a valid MP4 file before processing.
                file_count += 1
                
                input_file_path = os.path.join(root, filename)
                print(f"Processing ({file_count}/{file_limit}): {input_file_path}")
                
                # Get the video's duration.
                duration = get_video_duration(input_file_path)
                
                if duration is None or duration < 20: # Ensure video is long enough
                    print(f"Skipping '{filename}' as it's too short or duration could not be determined.")
                    continue
                
                # Calculate the start times for the three samples.
                # The start time is calculated from the start of the video.
                start_times = {
                    "sample_1": duration * 0.50,
                    "sample_2": duration * 0.75,
                    "sample_3": duration * 0.90
                }

                # Get the base filename without the extension for the output name.
                base_name = os.path.splitext(filename)[0]
                
                # Iterate through the calculated start times and create the samples.
                for i, (sample_name, start_time) in enumerate(start_times.items(), 1):
                    # Construct the new filename based on the specified format.
                    output_filename = f"{base_name}-sample ({i}).mp4"
                    output_file_path = os.path.join(OUTPUT_DIR, output_filename)
                    
                    # Call the function to create the video sample.
                    create_video_sample(input_file_path, output_file_path, start_time)

    print("\nVideo sampling process complete.")


# Run the main function.
if __name__ == "__main__":
    main()
