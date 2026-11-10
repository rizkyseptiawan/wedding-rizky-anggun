import re
import urllib.request
import os
import json

with open("page_raw.html", "r", encoding="utf-8") as f:
    c = f.read()

links = re.findall(r'https?://(?:img|media)\.katsudoto\.id/[^\s"\'\(\)<>]+', c)
cleaned_links = []
for l in links:
    clean = l.replace('\\/', '/').rstrip('\\')
    if clean and not clean.endswith('.mp3'):
        cleaned_links.append(clean)

unique_links = sorted(list(set(cleaned_links)))
print(f"Total media/img links found: {len(unique_links)}")

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Referer": "https://annajeremiah.katsudoto.id/107754"
}

os.makedirs("assets/img/photos", exist_ok=True)
url_to_local_photo = {}

for i, l in enumerate(unique_links):
    if ".webp" in l:
        ext = ".webp"
    elif ".jpg" in l or ".jpeg" in l:
        ext = ".jpg"
    elif ".svg" in l:
        ext = ".svg"
    else:
        ext = ".png"

    fname = f"photo_{i:02d}{ext}"
    target = f"assets/img/photos/{fname}"
    if not os.path.exists(target) or os.path.getsize(target) == 0:
        try:
            req = urllib.request.Request(l, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as r:
                data = r.read()
                with open(target, "wb") as f:
                    f.write(data)
            print(f"[OK] {fname} ({len(data)} bytes) from {l[:60]}...")
        except Exception as e:
            print(f"[ERR] {fname}: {e} for {l}")
            continue

    url_to_local_photo[l] = target
    url_to_local_photo[l.replace('/', '\\/')] = target

with open("photo_map.json", "w", encoding="utf-8") as f:
    json.dump(url_to_local_photo, f, indent=2)

print(f"Saved photo map with {len(url_to_local_photo)} entries!")
