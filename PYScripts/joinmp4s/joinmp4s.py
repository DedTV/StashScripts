import os
import subprocess
import shutil

def join_massive_files_safe():
    output_name = "final_output.mp4"
    temp_dir = "temp_processing"
    manifest_path = "manifest.txt"

    # 1. Workspace Setup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    # 2. Get files - handling encoding carefully
    # We use os.scandir for better performance with hundreds of files
    video_files = []
    with os.scandir('.') as it:
        for entry in it:
            if entry.is_file() and entry.name.lower().endswith('.mp4') and entry.name != output_name:
                video_files.append(entry.name)
    
    video_files.sort()

    if not video_files:
        print("No MP4 files found.")
        return

    print(f"🚀 Found {len(video_files)} files. Processing with NVENC...")

    # 3. Phase 1: Standardize using numeric placeholders
    for i, original_name in enumerate(video_files):
        # We use a safe numeric name for the target to avoid encoding issues
        target_ts = os.path.join(temp_dir, f"{i:05d}.ts")
        
        args = [
            "ffmpeg", "-y",
            "-i", original_name,
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "-c:v", "hevc_nvenc", "-cq", "26", "-preset", "p4", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-ar", "44100", "-ac", "2",
            "-f", "mpegts", target_ts
        ]
        
        print(f"[{i+1}/{len(video_files)}] Processing segment...")
        
        try:
            # We use shell=False to pass the raw list to the API
            subprocess.run(args, check=True, shell=False)
        except Exception as e:
            print(f"❌ Failed on file: {repr(original_name)}")
            print(f"Error: {e}")
            continue

    # 4. Phase 2: Create Manifest with safe paths
    print("\n📝 Creating join manifest...")
    with open(manifest_path, "w", encoding="utf-8") as f:
        for i in range(len(video_files)):
            # Reference the safe numeric names
            f.write(f"file '{temp_dir}/{i:05d}.ts'\n")

    # 5. Phase 3: Concatenate
    print("🔗 Stitching all segments...")
    final_args = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", manifest_path,
        "-c", "copy",
        output_name
    ]
    
    try:
        subprocess.run(final_args, check=True, shell=False)
        print(f"\n✅ Success! Saved as {output_name}")
    finally:
        # 6. Cleanup
        if os.path.exists(manifest_path):
            os.remove(manifest_path)
        # shutil.rmtree(temp_dir) # Uncomment to delete the temp folder

if __name__ == "__main__":
    join_massive_files_safe()