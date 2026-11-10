from html.parser import HTMLParser
import re

with open("page_raw.html", "r", encoding="utf-8") as f:
    html = f.read()

# Extract quote
quotes = re.findall(r'<section class="quote-wrap[^"]*">(.*?)</section>', html, re.DOTALL)
if quotes:
    print("--- QUOTE ---")
    print(re.sub(r'<[^>]+>', ' ', quotes[0]).strip())

# Extract couple
couple = re.findall(r'<section class="couple-wrap[^"]*">(.*?)</section>', html, re.DOTALL)
if couple:
    print("\n--- COUPLE ---")
    print(re.sub(r'<[^>]+>', ' ', couple[0]).strip())

# Extract story
story = re.findall(r'<section class="love-story[^"]*">(.*?)</section>', html, re.DOTALL)
if story:
    print("\n--- STORY ---")
    print(re.sub(r'<[^>]+>', ' ', story[0]).strip())

# Extract agenda
agenda = re.findall(r'<section class="agenda-wrap[^"]*">(.*?)</section>', html, re.DOTALL)
if agenda:
    print("\n--- AGENDA ---")
    print(re.sub(r'<[^>]+>', ' ', agenda[0]).strip())

# Extract gift / banks
gift = re.findall(r'<section class="[^"]*wedding-gift[^"]*">(.*?)</section>', html, re.DOTALL)
if gift:
    print("\n--- GIFT ---")
    print(re.sub(r'<[^>]+>', ' ', gift[0]).strip()[:500])

# Extract thank you
ty = re.findall(r'<section class="ty-wrap[^"]*">(.*?)</section>', html, re.DOTALL)
if ty:
    print("\n--- THANK YOU ---")
    print(re.sub(r'<[^>]+>', ' ', ty[0]).strip())
