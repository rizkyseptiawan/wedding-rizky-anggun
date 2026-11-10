import re
import os
import urllib.request
import urllib.parse
import hashlib

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://annajeremiah.katsudoto.id/107754",
    "Accept": "*/*"
}

with open("page_raw.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find all image links in html
urls = []
for m in re.finditer(r'(https?://[^\s"\'<>\(\)]+?\.(?:png|jpg|jpeg|webp|gif|svg))', html, re.IGNORECASE):
    urls.append(m.group(1))

# Also unescape \/
html_unescaped = html.replace('\\/', '/')
for m in re.finditer(r'(https?://[^\s"\'<>\(\)]+?\.(?:png|jpg|jpeg|webp|gif|svg))', html_unescaped, re.IGNORECASE):
    urls.append(m.group(1))

# Also media.katsudoto and img.katsudoto urls even without obvious extension
for m in re.finditer(r'(https?://(?:img|media)\.katsudoto\.id/[^\s"\'<>\(\)]+)', html_unescaped):
    urls.append(m.group(1))

# Relative paths
for m in re.finditer(r'[\'"](/media/[^\s"\'<>\(\)]+?\.(?:png|jpg|jpeg|webp|gif|svg))[\'"]', html_unescaped, re.IGNORECASE):
    urls.append("https://annajeremiah.katsudoto.id" + m.group(1))

unique_urls = list(dict.fromkeys(urls))
print(f"Total image targets to verify: {len(unique_urls)}")

failed = []
success = 0
for u in unique_urls:
    h = hashlib.md5(u.encode()).hexdigest()[:8]
    parsed = urllib.parse.urlparse(u)
    ext = os.path.splitext(parsed.path)[1]
    if not ext or ext.lower() not in ['.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif']:
        ext = ".png"
    target = f"assets/img/img_{h}{ext}"
    if os.path.exists(target) and os.path.getsize(target) > 0:
        success += 1
        continue
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            with open(target, "wb") as f:
                f.write(data)
        success += 1
        print(f"[OK] {u} -> {target}")
    except Exception as e:
        failed.append((u, str(e)))

print(f"\nDone: {success} successfully present in assets/img/.")
if failed:
    print(f"Failed {len(failed)} items:")
    for u, err in failed[:10]:
        print(f"  {u}: {err}")
