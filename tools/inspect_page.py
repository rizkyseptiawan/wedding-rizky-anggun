import re
from html.parser import HTMLParser

with open("page_raw.html", "r", encoding="utf-8") as f:
    html = f.read()

class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.css = []
        self.scripts = []
        self.imgs = []
        self.audio = []
        self.sources = []
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "link" and attr_dict.get("rel") == "stylesheet":
            if "href" in attr_dict:
                self.css.append(attr_dict["href"])
        elif tag == "script" and "src" in attr_dict:
            self.scripts.append(attr_dict["src"])
        elif tag == "img" and "src" in attr_dict:
            self.imgs.append(attr_dict["src"])
        elif tag == "audio" and "src" in attr_dict:
            self.audio.append(attr_dict["src"])
        elif tag == "source" and "src" in attr_dict:
            self.sources.append(attr_dict["src"])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data

parser = AssetParser()
parser.feed(html)

print("Title:", parser.title.strip())

print(f"\n--- CSS Links ({len(parser.css)}): ---")
for c in parser.css:
    print(c)

print(f"\n--- Script Sources ({len(parser.scripts)}): ---")
for s in parser.scripts:
    print(s)

print(f"\n--- Images ({len(parser.imgs)}): ---")
for img in parser.imgs[:25]:
    print(img)
if len(parser.imgs) > 25:
    print(f"... and {len(parser.imgs)-25} more images")

print("\n--- Audio / MP3: ---")
print("Audio tags:", parser.audio)
print("Source tags:", parser.sources)
mp3s = list(set(re.findall(r"https?://[^\s\"\'\(\)]+\.mp3[^\s\"\'\(\)]*", html)))
print("MP3 matches in html:", mp3s)

bg_imgs = list(set(re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', html)))
print(f"\n--- CSS url() references ({len(bg_imgs)}): ---")
for b in bg_imgs:
    print(b)

# Also let's search for music player variables or javascript audio objects
audio_matches = re.findall(r'[^\n]*music[^\n]*', html, re.IGNORECASE)
print(f"\n--- 'music' lines in html ({len(audio_matches)}): ---")
for m in audio_matches[:10]:
    print(m.strip())
