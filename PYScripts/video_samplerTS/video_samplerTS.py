import sys
import json
import os
import subprocess
from datetime import timedelta
from stashapi.stashapp import StashInterface
import io

# Force UTF-8 encoding for standard output to handle emojis in filenames
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# --- CONFIGURATION ---
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
FFPROBE_PATH = r"C:\ffmpeg\bin\ffprobe.exe"
OUTPUT_DIR = r"F:\Clips"
SAMPLE_DURATION = 30

# Define your sample points here as decimals (e.g., 0.25 = 25%)
SAMPLE_PERCENTAGES = [0.50, 0.75, 0.90]
# ---------------------

def get_video_duration(video_path):
    try:
        cmd = [
            FFPROBE_PATH, "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error probing {video_path}: {e}")
        return None

def create_video_sample(input_path, output_path, start_time_seconds):
    try:
        # Format start time for FFmpeg
        start_time_formatted = str(timedelta(seconds=start_time_seconds))
        
        # Standardized command to match your unifymp4s.py workflow
        cmd = [
            FFMPEG_PATH, "-y",
            "-ss", start_time_formatted,
            "-i", input_path,
            "-t", str(SAMPLE_DURATION),
            # Video: Scale, Pad to 1080p, and force 30fps
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30",
            "-c:v", "hevc_nvenc", "-cq", "24", "-preset", "p4", "-pix_fmt", "yuv420p",
            # Audio: Force sync and standardize to 48kHz
            "-af", "aresample=async=1:min_hard_comp=0.1:first_pts=0",
            "-c:a", "aac", "-ar", "48000", "-ac", "2",
            # Join-safety flags
            "-avoid_negative_ts", "make_zero",
            "-map_metadata", "-1",
            "-muxdelay", "0",
            "-f", "mpegts",
            output_path
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except Exception as e:
        print(f"FFmpeg error on {input_path}: {e}")
        return False

def process_scenes(stash, scenes):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    total = len(scenes)
    if total == 0:
        print("No scenes found matching the criteria.")
        return

    print(f"Starting standardized sampling for {total} scenes.")

    for idx, scene in enumerate(scenes):
        files = scene.get("files", [])
        if not files:
            continue

        input_file_path = files[0].get("path")
        # Extract base name from input path
        base_name = os.path.splitext(os.path.basename(input_file_path))[0]
        
        duration = get_video_duration(input_file_path)
        
        if not duration or duration < (max(SAMPLE_PERCENTAGES) * duration) + SAMPLE_DURATION:
            print(f"Skipping {base_name}: Video too short.")
            continue

        print(f"[{idx+1}/{total}] Exporting TS Samples: {base_name}")

        for i, pct in enumerate(SAMPLE_PERCENTAGES, 1):
            start_time = duration * pct
            
            if start_time > duration - SAMPLE_DURATION:
                start_time = duration - SAMPLE_DURATION

            # Using .ts extension for direct compatibility with joinmp4.py
            output_filename = f"{base_name}-sample ({i}).ts"
            output_file_path = os.path.join(OUTPUT_DIR, output_filename)
            
            create_video_sample(input_file_path, output_file_path, start_time)

def main():
    try:
        input_data = json.load(sys.stdin)
    except:
        input_data = {}

    stash = StashInterface(input_data.get("server_connection", {}))
    args = input_data.get("args", {})
    mode = args.get("mode")

    scenes = []
    all_pages_filter = {"per_page": -1}

    if mode == "rated":
        scenes = stash.find_scenes(f={"rating100": {"value": 100, "modifier": "EQUALS"}}, filter=all_pages_filter)
    elif mode == "three_star":
        scenes = stash.find_scenes(f={"rating100": {"value": 60, "modifier": "EQUALS"}}, filter=all_pages_filter) 
    elif mode == "tag":
        tag_id = "15" # Set your desired Tag ID here
        id_query = """
        query FindSceneIds($tag_id: [ID!]) {
          findScenes(scene_filter: {tags: {value: $tag_id, modifier: INCLUDES}}, filter: {per_page: -1}) {
            scenes { id }
          }
        }
        """
        id_result = stash.call_GQL(id_query, {"tag_id": [tag_id]})
        all_ids = [s['id'] for s in id_result['findScenes']['scenes']]
        
        for s_id in all_ids:
            scene_data = stash.find_scene(s_id)
            if scene_data:
                scenes.append(scene_data)
    elif mode == "all":
        scenes = stash.find_scenes(filter=all_pages_filter)
    
    process_scenes(stash, scenes)

if __name__ == "__main__":
    main()