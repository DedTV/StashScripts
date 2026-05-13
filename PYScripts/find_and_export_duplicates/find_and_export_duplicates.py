import sqlite3
import os

# --- Configuration ---
DATABASE_PATH = r'E:\stash-go.sqlite'
OUTPUT_PATH = r'e:\Duplicates.txt'

def find_and_export_duplicates():
    """
    Connects to the SQLite database, finds exact duplicate scene titles,
    and exports their ID and Title to a tab-separated text file.
    """
    conn = None
    try:
        # 1. Connect to the SQLite database
        print(f"Connecting to database: {DATABASE_PATH}")
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # 2. SQL Query to find all records associated with a duplicate title.
        # This subquery finds all titles that appear more than once.
        # The main query then selects all ID/Title pairs for those duplicated titles.
        sql_query = """
        SELECT id, title
        FROM scenes
        WHERE title IN (
            SELECT title
            FROM scenes
            GROUP BY title
            HAVING COUNT(title) > 1
        )
        ORDER BY title, id;
        """

        cursor.execute(sql_query)
        duplicate_records = cursor.fetchall()
        
        print(f"Found {len(duplicate_records)} records belonging to duplicate titles.")

        if not duplicate_records:
            print("No duplicate scene titles found.")
            # Create an empty file with a message if none are found, just to confirm operation
            with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
                f.write("No exact duplicate scene titles were found.\n")
            print(f"Output file created at {OUTPUT_PATH} (empty/message).")
            return

        # 3. Write results to the tab-separated file
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as outfile:
            # Write header row, tab-separated
            outfile.write("ID\tTitle\n")
            
            # Write data rows
            for record_id, title in duplicate_records:
                # Use tab (\t) for separation
                outfile.write(f"{record_id}\t{title}\n")
        
        print(f"\nSuccessfully exported duplicates to:\n{OUTPUT_PATH}")

    except sqlite3.Error as e:
        print(f"\nDatabase Error occurred: {e}")
        print(f"Please check if the database file exists at '{DATABASE_PATH}' and is not locked.")
    except IOError as e:
        print(f"\nFile System Error occurred: {e}")
        print(f"Could not write to the output path '{OUTPUT_PATH}'. Check file permissions or if the E: drive is mounted.")
    finally:
        # 4. Close the connection
        if conn:
            conn.close()

if __name__ == "__main__":
    # Ensure the script runs only when executed directly
    find_and_export_duplicates()
