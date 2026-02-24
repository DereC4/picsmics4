import json
import os
from yt_dlp import YoutubeDL

url = "https://www.youtube.com/watch?v=lW7vWfRI5oI"
original_path = "docs/comments_ORIGINAL.json" # the original, authentic comments from before cutoff (in case they get edited/deleted one day)
output_path = "docs/comments.json"
CUTOFF = 1767247567  # Jan 1 2026 UTC at SIX SEVEN

# Load the frozen original comments (pre-cutoff, never modified)
original = json.load(open(original_path, encoding="utf-8")) if os.path.exists(original_path) else []
# ^^ this is a LONG ternary btw

with YoutubeDL({"skip_download": True, "getcomments": True}) as ydl:
    scraped = ydl.extract_info(url, download=False).get("comments", [])

new_by_id = {}
for c in scraped:
    if c.get("timestamp", 0) >= CUTOFF and c.get("id"):
        new_by_id[c["id"]] = c

# we'll grab comments that are after the cutoff, those are what will be appended

merged = original + sorted(new_by_id.values(), key=lambda x: x.get("timestamp", 0))

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)


print(f"Done\n{len(original)} original comments + {len(new_by_id)} new comments = {len(merged)} total")