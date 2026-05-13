import sqlite3
import os

DB_PATH = r"E:\stash-go.sqlite"

def prepare():
    print("--- Phase 1: Prepare for Identify ---")
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Create tracker table
        cursor.execute("CREATE TABLE IF NOT EXISTS tmp_organized_tracker (scene_id INTEGER PRIMARY KEY)")
        
        # SAFETY: Check if tracker already has data
        cursor.execute("SELECT count() FROM tmp_organized_tracker")
        if cursor.fetchone()[0] > 0:
            print("ABORT: A backup already exists. You must run the Restore script before running Prepare again.")
            return

        # Get organized scenes
        cursor.execute("SELECT id FROM scenes WHERE organized = 1")
        ids = [row[0] for row in cursor.fetchall()]

        if not ids:
            print("No organized scenes (1) found to process.")
            return

        print(f"Backing up {len(ids)} IDs...")
        cursor.executemany("INSERT INTO tmp_organized_tracker (scene_id) VALUES (?)", [(id,) for id in ids])
        
        print("Setting scenes to Unorganized (0)...")
        cursor.execute("UPDATE scenes SET organized = 0 WHERE organized = 1")
        
        conn.commit()
        print(f"SUCCESS: {len(ids)} scenes are now ready for the Identify task.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    prepare()