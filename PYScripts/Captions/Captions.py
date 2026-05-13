import os
import concurrent.futures
from faster_whisper import WhisperModel

# --- CONFIGURATION ---
SOURCE_DIR = r"F:\stashed"
MODEL_SIZE = "large-v3" 
DEVICE = "cuda"
COMPUTE_TYPE = "float16"
TIMEOUT_SECONDS = 600  # 10 Minutes per file

def format_timestamp(seconds: float):
    td_hours = int(seconds // 3600)
    td_mins = int((seconds % 3600) // 60)
    td_secs = int(seconds % 60)
    td_msecs = int((seconds - int(seconds)) * 1000)
    return f"{td_hours:02}:{td_mins:02}:{td_secs:02},{td_msecs:03}"

def process_file(model, video_path, srt_path):
    """
    Internal function to handle the actual transcription logic.
    """
    segments, info = model.transcribe(
        video_path, 
        task="translate", 
        word_timestamps=True,
        beam_size=5
    )

    with open(srt_path, "w", encoding="utf-8") as srt:
        counter = 1
        for segment in segments:
            if not segment.words:
                continue
            
            # Grouping words into short, readable chunks (max 5 words or 30 chars)
            current_chunk = []
            char_count = 0
            
            for word in segment.words:
                current_chunk.append(word)
                char_count += len(word.word)
                
                if len(current_chunk) >= 5 or char_count >= 30:
                    start = format_timestamp(current_chunk[0].start)
                    end = format_timestamp(current_chunk[-1].end)
                    text = "".join([w.word for w in current_chunk]).strip()
                    
                    srt.write(f"{counter}\n{start} --> {end}\n{text}\n\n")
                    
                    counter += 1
                    current_chunk = []
                    char_count = 0
            
            # Write any remaining words in the last chunk
            if current_chunk:
                start = format_timestamp(current_chunk[0].start)
                end = format_timestamp(current_chunk[-1].end)
                text = "".join([w.word for w in current_chunk]).strip()
                srt.write(f"{counter}\n{start} --> {end}\n{text}\n\n")
                counter += 1

def transcribe_directory(path):
    print(f"Initializing {MODEL_SIZE} on RTX 4060...")
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(".mp4"):
                video_path = os.path.join(root, file)
                srt_path = os.path.splitext(video_path)[0] + ".srt"
                if os.path.exists(srt_path): continue

                print(f"🚀 Processing: {file}")
                
                # Using ThreadPoolExecutor to enforce the timeout
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(process_file, model, video_path, srt_path)
                    try:
                        future.result(timeout=TIMEOUT_SECONDS)
                        print(f"✅ Saved: {file}")
                    except concurrent.futures.TimeoutError:
                        print(f"❌ TIMEOUT: {file} took longer than 10 minutes. Skipping...")
                        # We can't easily kill a thread in Python, but we can stop waiting for it.
                    except Exception as e:
                        print(f"❌ ERROR: {file} failed with: {e}")

if __name__ == "__main__":
    if not os.path.exists(SOURCE_DIR):
        print(f"Error: {SOURCE_DIR} not found.")
    else:
        transcribe_directory(SOURCE_DIR)