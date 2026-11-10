import os
import re
import urllib.request
import urllib.parse
import hashlib

ORIGIN = "https://annajeremiah.katsudoto.id"
BASE_URL = "https://annajeremiah.katsudoto.id/107754"

os.makedirs("assets/css", exist_ok=True)
os.makedirs("assets/js", exist_ok=True)
os.makedirs("assets/img", exist_ok=True)
os.makedirs("assets/audio", exist_ok=True)
os.makedirs("assets/fonts", exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": BASE_URL,
    "Accept": "*/*"
}

def resolve_url(u, context_url=BASE_URL):
    u = u.replace("\\/", "/").strip()
    if u.startswith("//"):
        return "https:" + u
    elif u.startswith("/"):
        return ORIGIN + u
    elif not u.startswith("http"):
        return urllib.parse.urljoin(context_url, u)
    return u

def download_file(url, target_path):
    if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
        return True
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=25) as resp:
            content = resp.read()
            with open(target_path, "wb") as out:
                out.write(content)
        print(f"[OK] Downloaded: {url} -> {target_path}")
        return True
    except Exception as e:
        print(f"[ERR] Failed {url}: {e}")
        return False

with open("page_raw.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Download Audio
mp3_urls = list(set(re.findall(r'https?://[^\s"\'\(\)]+?\.(?:mp3|ogg|m4a)[^\s"\'\(\)]*', html)))
audio_map = {}
for mp3 in mp3_urls:
    clean_url = mp3.replace("\\/", "/")
    parsed = urllib.parse.urlparse(clean_url)
    fname = os.path.basename(parsed.path) or "wedding-audio.mp3"
    local_path = os.path.join("assets/audio", fname)
    if download_file(clean_url, local_path):
        audio_map[clean_url] = f"assets/audio/{fname}"
        audio_map[mp3] = f"assets/audio/{fname}"

# 2. Extract and download CSS
css_matches = re.findall(r'<link[^>]+rel=[\'"]stylesheet[\'"][^>]+href=[\'"]([^\'"]+)[\'"]', html)
css_matches += re.findall(r'<link[^>]+href=[\'"]([^\'"]+)[\'"][^>]+rel=[\'"]stylesheet[\'"]', html)
css_map = {}

for u in list(dict.fromkeys(css_matches)):
    full_url = resolve_url(u)
    parsed = urllib.parse.urlparse(full_url)
    base_name = os.path.basename(parsed.path) or "style.css"
    h = hashlib.md5(full_url.encode()).hexdigest()[:6]
    local_name = f"{h}_{base_name}"
    if not local_name.endswith(".css"):
        local_name += ".css"
    local_path = os.path.join("assets/css", local_name)
    if download_file(full_url, local_path):
        css_map[u] = f"assets/css/{local_name}"

# 3. Extract and download JS
js_matches = re.findall(r'<script[^>]+src=[\'"]([^\'"]+)[\'"]', html)
js_map = {}
for u in list(dict.fromkeys(js_matches)):
    full_url = resolve_url(u)
    parsed = urllib.parse.urlparse(full_url)
    base_name = os.path.basename(parsed.path) or "script.js"
    h = hashlib.md5(full_url.encode()).hexdigest()[:6]
    local_name = f"{h}_{base_name}"
    if not local_name.endswith(".js"):
        local_name += ".js"
    local_path = os.path.join("assets/js", local_name)
    if download_file(full_url, local_path):
        js_map[u] = f"assets/js/{local_name}"

# 4. Extract and download all images from HTML
img_matches = []
img_matches += re.findall(r'(?:src|data-src|data-original|href)=[\'"]([^\'"]+\.(?:png|jpg|jpeg|webp|gif|svg)[^\'"]*)[\'"]', html, re.IGNORECASE)
img_matches += re.findall(r'https?://(?:img|media)\.katsudoto\.id/[^\s"\'\(\)<>]+', html)
img_matches += re.findall(r'https?://[^\s"\'\(\)<>]+\.(?:png|jpg|jpeg|webp|svg|gif)', html, re.IGNORECASE)
img_matches += re.findall(r'url\([\'"]?([^\'"\)]+\.(?:png|jpg|jpeg|webp|svg|gif)[^\'"\)]*)[\'"]?\)', html, re.IGNORECASE)
# Template assets
img_matches += re.findall(r'/(?:media|img|assets)/[^\s"\'\(\)<>]+\.(?:png|jpg|jpeg|webp|svg|gif)', html, re.IGNORECASE)

clean_imgs = []
for u in img_matches:
    u_clean = u.replace("\\/", "/").strip()
    if u_clean and not u_clean.startswith("data:") and not u_clean.endswith(".mp3"):
        clean_imgs.append(u_clean)

img_map = {}
for u in list(dict.fromkeys(clean_imgs)):
    full_url = resolve_url(u)
    parsed = urllib.parse.urlparse(full_url)
    ext = os.path.splitext(parsed.path)[1]
    if not ext or ext.lower() not in ['.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif']:
        ext = ".png"
    h = hashlib.md5(full_url.encode()).hexdigest()[:8]
    local_name = f"img_{h}{ext}"
    local_path = os.path.join("assets/img", local_name)
    if download_file(full_url, local_path):
        img_map[u] = f"assets/img/{local_name}"
        # also map unescaped/escaped versions
        img_map[u.replace("/", "\\/")] = f"assets/img/{local_name}"
        img_map[full_url] = f"assets/img/{local_name}"
        img_map[full_url.replace("/", "\\/")] = f"assets/img/{local_name}"

# 5. Extract internal resources inside downloaded CSS files (fonts, images)
print("\n--- Scanning CSS files for fonts and background images ---")
font_map = {}
for css_file in os.listdir("assets/css"):
    css_path = os.path.join("assets/css", css_file)
    with open(css_path, "r", encoding="utf-8", errors="ignore") as f:
        css_text = f.read()

    css_urls = re.findall(r'url\([\'"]?([^\'"\)]+)[\'"]?\)', css_text)
    modified = False
    for cu in set(css_urls):
        cu_clean = cu.strip().strip("'\"")
        if cu_clean.startswith("data:") or cu_clean.startswith("#"):
            continue
        full_cu = resolve_url(cu_clean)
        parsed = urllib.parse.urlparse(full_cu)
        ext = os.path.splitext(parsed.path)[1]
        
        if any(e in ext.lower() for e in ['.woff2', '.woff', '.ttf', '.otf', '.eot']):
            # Font
            h = hashlib.md5(full_cu.encode()).hexdigest()[:6]
            bname = os.path.basename(parsed.path)
            local_fname = f"{h}_{bname}"
            target_fpath = os.path.join("assets/fonts", local_fname)
            if download_file(full_cu, target_fpath):
                rel_from_css = f"../fonts/{local_fname}"
                css_text = css_text.replace(cu, rel_from_css)
                modified = True
        elif any(e in ext.lower() for e in ['.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif']):
            # Image in CSS
            h = hashlib.md5(full_cu.encode()).hexdigest()[:8]
            local_iname = f"img_{h}{ext}"
            target_ipath = os.path.join("assets/img", local_iname)
            if download_file(full_cu, target_ipath):
                rel_from_css = f"../img/{local_iname}"
                css_text = css_text.replace(cu, rel_from_css)
                modified = True

    if modified:
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(css_text)

print(f"\nAsset collection finished! Total assets ready.")
