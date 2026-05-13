import sqlite3
import re

# Connect to your database
conn = sqlite3.connect('stash-go.sqlite')
cursor = conn.cursor()

# 1. Fetch the IDs and URLs that contain potential junk
# We look for common markers like backslashes or the duration tag
cursor.execute("SELECT rowid, url FROM scene_urls WHERE url LIKE '%\\%' OR url LIKE '%duration%'")
rows = cursor.fetchall()

for rowid, raw_url in rows:
    # Regex to keep only printable ASCII characters (32-126)
    # This strips \x01, \x02, and the 'ï¿½' artifacts
    clean_url = re.sub(r'[^\x20-\x7E]', '', raw_url)
    
    # Optional: If the "duration" text is still there, split it off
    # URLs on that site usually don't need anything after the slug
    if 'duration' in clean_url:
        clean_url = clean_url.split('duration')[0].rstrip(';')

    # 2. Update the record
    cursor.execute("UPDATE scene_urls SET url = ? WHERE rowid = ?", (clean_url, rowid))

conn.commit()
conn.close()
print(f"Cleaned {len(rows)} URLs.")