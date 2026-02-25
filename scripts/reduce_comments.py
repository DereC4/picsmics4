import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "..", "docs", "comments.json")
output_path = os.path.join(script_dir, "..", "docs", "comments_reduced.json")

with open(input_path, "r", encoding="utf-8") as f:
    comments = json.load(f)

reduced = [
    {
        "author": c["author"],
        "text": c["text"],
        "time": c.get("_time_text", "Unknown"),
    }
    for c in comments
]

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(reduced, f, indent=2, ensure_ascii=False)

print(f"Reduced {len(comments)} comments -> {output_path}")
