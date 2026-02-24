import json

comments = json.load(open("docs/comments.json", encoding="utf-8"))
seen, dupes = {}, 0

for i, c in enumerate(comments):
    k = (c.get("id",""), c.get("text",""), c.get("timestamp",0))
    if k in seen: 
        dupes += 1; 
        print(f"  Index {i} dupes {seen[k]} | id={k[0]} | ts={k[2]} | text={k[1][:80]}")
    else: 
        seen[k] = i

print(f"Found {dupes} duplicate(s)" if dupes else f"No duplicates among us.")