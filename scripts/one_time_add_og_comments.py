# this was AI generated because I am feeling lazy and have a cold right now

import json
import os
from html import escape

script_dir = os.path.dirname(os.path.abspath(__file__))
original_path = os.path.join(script_dir, "..", "docs", "comments_ORIGINAL.json")
index_path = os.path.join(script_dir, "..", "docs", "index.html")

with open(original_path, "r", encoding="utf-8") as f:
    all_comments = json.load(f)

# Cutoff: hardcode only comments BEFORE "picsmics4 is one of the greatest examples..."
CUTOFF_ID = "UgywI-n-fC13yEtXzud4AaABAg"
cutoff_index = next(
    (i for i, c in enumerate(all_comments) if c.get("id") == CUTOFF_ID),
    None
)
if cutoff_index is None:
    print("ERROR: Cutoff comment not found in comments_ORIGINAL.json. Aborting.")
    exit(1)

comments = all_comments[:cutoff_index]
print(f"Cutoff found at index {cutoff_index}. Using {len(comments)} comments.")

def format_likes(count):
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    if count >= 1_000:
        n = count / 1000
        return f"{n:.0f}K" if count >= 10_000 else f"{n:.1f}K"
    return str(count)

# fix because we used linux formatting codes
def format_date(timestamp):
    from datetime import datetime, timezone
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return dt.strftime("%B %d, %Y").replace(" 0", " ")  # e.g. "January 2, 2008"

def format_tooltip_date(timestamp):
    from datetime import datetime, timezone
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    raw = dt.strftime("%A, %B %d, %Y, %I:%M:%S %p")
    return raw.replace(" 0", " ").replace(", 0", ", ")  # strip leading zeros

def build_comment_html(comment):
    badges = ""
    if comment.get("is_pinned"):
        badges += '<span class="stat-badge pinned-badge">📌 Pinned</span>'

    author = escape(comment.get("author", ""))
    author_url = escape(comment.get("author_url", "#"))
    author_thumbnail = escape(comment.get("author_thumbnail", ""))
    text = escape(comment.get("text", "")).replace("\n", "&#10;")
    like_count = comment.get("like_count", 0)
    time_text = escape(comment.get("_time_text", "Unknown"))
    timestamp = comment.get("timestamp", 0)

    likes_fmt = format_likes(like_count)
    date_fmt = format_date(timestamp) if timestamp else "Unknown"
    tooltip_fmt = format_tooltip_date(timestamp) if timestamp else ""

    return f"""        <li>
          <div class="comment">
            <div class="avatar">
              <a href="{author_url}" target="_blank" rel="noopener noreferrer">
                <img src="{author_thumbnail}" alt="{author}">
              </a>
            </div>
            <div class="comment__wrapper">
              <div class="comment__body">
                <a href="{author_url}" target="_blank" rel="noopener noreferrer" class="comment__author">{author}</a>
                <p class="comment__text" dir="auto">{text}</p>
              </div>
              <div class="comment__stats">
                {badges}
              </div>
              <div class="comment__meta">
                <span class="comment__likes">👍 {likes_fmt}</span>
                <span class="comment__time" title="{tooltip_fmt}">{time_text}</span>
              </div>
            </div>
          </div>
        </li>"""

print(f"Building HTML for {len(comments)} original comments...")
items_html = "\n".join(build_comment_html(c) for c in comments)

new_ul = f'<ul id="comments-list">\n{items_html}\n      </ul>'

with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

OLD_UL = '<ul id="comments-list"></ul>'
if OLD_UL not in html:
    print("ERROR: Could not find '<ul id=\"comments-list\"></ul>' in index.html.")
    print("Has this script already been run? Aborting.")
    exit(1)

html = html.replace(OLD_UL, new_ul)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Done! {len(comments)} comments baked into index.html.")
print("The JS will now only dynamically append new (post-cutoff) comments.")