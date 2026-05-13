import sqlite3
from titlecase import titlecase
import sys

# --- Configuration ---
# The path to your SQLite database file.
# Note on Windows paths: If your path contains backslashes (e.g., 'E:\stash-go.sqlite'),
# use a raw string (r'E:\stash-go.sqlite') to avoid syntax warnings.
DATABASE_FILE = (r'E:\stash-go.sqlite')

def process_scene_titles():
    """
    Connects to the SQLite database, reads all scene titles,
    converts them to proper title case, and updates them in the database.
    """
    conn = None  # Initialize connection to None
    updated_count = 0
    processed_count = 0

    # A list of words to always keep in uppercase (e.g., acronyms).
    custom_abbreviations = ['USA', 'UK', 'FBI', 'CIA', 'CGI', 'DP']

    # This callback function handles custom abbreviations to ensure they remain uppercase.
    # It's used for compatibility with older versions of the 'titlecase' library
    # that don't support the 'abbreviations' keyword argument.
    def abbreviations_callback(word, all_caps):
        if word.upper() in custom_abbreviations:
            return word.upper()
        # Returning None tells the titlecase function to use its default behavior for the word.
        return None

    try:
        # Establish a connection to the SQLite database
        print(f"Connecting to database: {DATABASE_FILE}...")
        conn = sqlite3.connect(DATABASE_FILE)
        # Using a dictionary cursor makes it easier to access columns by name
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # --- Step 1: Fetch all scene records ---
        print("Fetching all scene titles from the database...")
        cursor.execute("SELECT id, title FROM scenes")
        scenes = cursor.fetchall()
        total_scenes = len(scenes)
        print(f"Found {total_scenes} scenes to process.")

        # --- Step 2: Process each title and update if necessary ---
        for scene in scenes:
            processed_count += 1
            original_title = scene['title']

            # Check if the title is None or an empty string
            if not original_title:
                print(f"Skipping Scene ID: {scene['id']} (title is empty)")
                continue

            # Convert the title to smart title case using the callback for abbreviations.
            corrected_title = titlecase(original_title, callback=abbreviations_callback)

            # --- Step 3: Update the database only if the title has changed ---
            if original_title != corrected_title:
                updated_count += 1
                print(f"Updating Scene ID: {scene['id']}")
                print(f"  - OLD: {original_title}")
                print(f"  + NEW: {corrected_title}")
                cursor.execute(
                    "UPDATE scenes SET title = ? WHERE id = ?",
                    (corrected_title, scene['id'])
                )

            # Provide progress update in the console
            if processed_count % 100 == 0:
                print(f"Processed {processed_count}/{total_scenes} scenes...")


        # --- Step 4: Commit the changes to the database ---
        if updated_count > 0:
            print("\nCommitting changes to the database...")
            conn.commit()
            print("Changes committed successfully.")
        else:
            print("\nNo titles needed updating.")

    except sqlite3.Error as e:
        # Handle potential database errors
        print(f"Database error: {e}", file=sys.stderr)
        if conn:
            # If an error occurs, roll back any changes made during the transaction
            print("Rolling back changes.", file=sys.stderr)
            conn.rollback()
    except FileNotFoundError:
        print(f"Error: The database file '{DATABASE_FILE}' was not found.", file=sys.stderr)
        print("Please ensure the script is in the same directory as the database or provide the correct path.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
    finally:
        # --- Step 5: Close the connection ---
        if conn:
            conn.close()
            print("\nDatabase connection closed.")
        
        print("\n--- Summary ---")
        print(f"Total scenes processed: {processed_count}")
        print(f"Total scenes updated: {updated_count}")
        print("---------------")


if __name__ == '__main__':
    # Before running, ensure you have the titlecase library installed:
    # pip install titlecase
    # If the script still fails, you may need to update it:
    # pip install --upgrade titlecase
    process_scene_titles()
