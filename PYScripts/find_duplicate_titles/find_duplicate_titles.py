import sqlite3

def find_duplicate_titles(db_path, output_file):
    """
    Connects to an SQLite database, scans the 'scenes.title' column for duplicates,
    and outputs the duplicate titles to a text file. Handles potential NoneType
    errors and diverse character sets.

    Args:
        db_path (str): The path to the SQLite database file.
        output_file (str): The path to the output text file.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to find duplicate titles
        cursor.execute("""
            SELECT title, COUNT(*)
            FROM scenes
            GROUP BY title
            HAVING COUNT(*) > 1
        """)

        duplicate_titles = [row[0] for row in cursor.fetchall()]

        if duplicate_titles:
            with open(output_file, 'w', encoding='utf-8') as f:  # Specify UTF-8 encoding
                for title in duplicate_titles:
                    if title is not None: #check for null/None values
                        f.write(str(title) + '\n') #cast to string to handle various data types
                    else:
                        f.write("NULL title found\n") #handle null values explicitly
            print(f"Duplicate titles found and written to {output_file}")
        else:
            print("No duplicate titles found.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Example usage:
db_path = r"e:\stash-go.sqlite"
output_file = "duplicate_titles.txt"

find_duplicate_titles(db_path, output_file)