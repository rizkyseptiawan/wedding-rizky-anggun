import os
import re
import urllib.request
import urllib.parse
import hashlib

BASE_URL = "https://annajeremiah.katsudoto.id/107754"
ORIGIN = "https://annajeremiah.katsudoto.id"

with open("page_raw.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Directories
os.makedirs("assets/css", exist_ok=True)
os.makedirs("assets/js", exist_ok=True)
os.makedirs("assets/img", exist_ok=True)
os.makedirs("assets/audio", exist_ok=True)
os.makedirs("assets/fonts", exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def download_file(url, target_path):
    if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
        return True
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read()
            with open(target_path, "wb") as out:
                out.write(content)
        print(f"[OK] Downloaded: {url} -> {target_path}")
        return True
    except Exception as e:
        print(f"[ERR] Failed {url}: {e}")
        return False

# 1. Download Audio
mp3_urls = list(set(re.findall(r'https?://[^\s"\'\(\)]+?\.(?:mp3|ogg|m4a)[^\s"\'\(\)]*', html_content)))
print("Found audio files:", mp3_urls)
for mp3 in mp3_urls:
    clean_url = mp3.replace("\\/", "/")
    fname = os.path.basename(urllib.parse.urlparse(clean_url).path)
    download_file(clean_url, os.path.join("assets/audio", fname))

# 2. Extract CSS links
css_matches = re.findall(r'<link[^>]+rel=[\'"]stylesheet[\'"][^>]+href=[\'"]([^\'"]+)[\'"]', html_content)
css_matches += re.findall(r'<link[^>]+href=[\'"]([^\'"]+)[\'"][^>]+rel=[\'"]stylesheet[\'"]', html_content)
css_urls = list(dict.fromkeys(css_matches))
print(f"Found {len(css_urls)} CSS links")

# 3. Extract Script sources
js_matches = re.findall(r'<script[^>]+src=[\'"]([^\'"]+)[\'"]', html_content)
js_urls = list(dict.fromkeys(js_matches))
print(f"Found {len(js_urls)} JS scripts")

# 4. Extract Images (img src, data-src, etc.)
img_matches = re.findall(r'(?:src|data-src|data-original|href)=[\'"]([^\'"]+\.(?:png|jpg|jpeg|webp|gif|svg)[^\'"]*)[\'"]', html_content, re.IGNORECASE)
img_matches += re.findall(r'https?://(?:img|media)\.katsudoto\.id/[^\s"\'\(\)<>]+', html_content)
# Also CSS background urls in html
inline_urls = re.findall(r'url\([\'"]?([^\'"\)]+)[\'"]?\)', html_content)
for u in inline_urls:
    if any(ext in u.lower() for ext in ['.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif']):
        img_matches.append(u)

# Filter unique image matches
all_raw_imgs = []
for u in img_matches:
    u = u.replace("\\/", "/").strip()
    if u and not u.startswith("data:"):
        all_raw_imgs.append(u)
all_imgs = list(dict.fromkeys(all_raw_imgs))
print(f"Found {len(all_imgs)} image references")

# Helper to resolve URL
def resolve_url(u):
    u = u.replace("\\/", "/")
    if u.startswith("//"):
        return "https:" + u
    elif u.startswith("/"):
        return ORIGIN + u
    elif not u.startswith("http"):
        return urllib.parse.urljoin(BASE_URL, u)
    return u

# Download CSS
css_map = {}
for u in css_urls:
    full_url = resolve_url(u)
    parsed = urllib.parse.urlparse(full_url)
    base_name = os.path.basename(parsed.path) or "style.css"
    # Make unique if needed
    h = hashlib.md5(full_url.encode()).hexdigest()[:6]
    local_name = f"{h}_{base_name}"
    local_path = os.path.join("assets/css", local_name)
    if download_file(full_url, local_path):
        css_map[u] = f"assets/css/{local_name}"

# Download JS
js_map = {}
for u in js_urls:
    full_url = resolve_url(u)
    parsed = urllib.parse.urlparse(full_url)
    base_name = os.path.basename(parsed.path) or "script.js"
    h = hashlib.md5(full_url.encode()).hexdigest()[:6]
    local_name = f"{h}_{base_name}"
    local_path = os.path.join("assets/js", local_name)
    if download_file(full_url, local_path):
        js_map[u] = f"assets/js/{local_name}"

# Download Images
img_map = {}
for u in all_imgs:
    full_url = resolve_url(u)
    parsed = urllib.parse.urlparse(full_url)
    path = parsed.path
    ext = os.path.splitext(path)[1]
    if not ext or ext.lower() not in ['.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif']:
        ext = ".png"
    h = hashlib.md5(full_url.encode()).hexdigest()[:8]
    local_name = f"img_{h}{ext}"
    local_path = os.path.join("assets/img", local_name)
    if download_file(full_url, local_path):
        img_map[u] = f"assets/img/{local_name}"

print(f"\nDownloaded: {len(css_map)} CSS, {len(js_map)} JS, {len(img_map)} Images.")
