import json
from yt_dlp import YoutubeDL

url = "https://www.youtube.com/watch?v=lW7vWfRI5oI"

with YoutubeDL({"skip_download": True, "getcomments": True}) as derexXD:
    info = derexXD.extract_info(url, download=False)

comments = sorted(info.get("comments", []), key=lambda x: x.get("timestamp", 0))

with open("docs/comments.json", "w") as file:
    json.dump(comments, file, indent=2)

print(f"Done\nExtracted {len(comments)} comments from el video (sorted oldest to newest)")
