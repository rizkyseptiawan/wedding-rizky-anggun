import re
import urllib.request
import os

with open("page_raw.html", "r", encoding="utf-8") as f:
    c = f.read()

fonts = set(re.findall(r'/cf-fonts/[^\s"\'\);]+', c))
print(f"Found {len(fonts)} cf-fonts")
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Referer": "https://annajeremiah.katsudoto.id/107754"
}

os.makedirs("assets/fonts", exist_ok=True)

for font_path in sorted(fonts):
    url = "https://annajeremiah.katsudoto.id" + font_path
    local_name = font_path.strip("/").replace("/", "_")
    target = os.path.join("assets/fonts", local_name)
    if not os.path.exists(target):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                with open(target, "wb") as out:
                    out.write(data)
            print(f"[OK] {font_path} -> {target}")
        except Exception as e:
            print(f"[ERR] {font_path}: {e}")

print("Font download finished!")
