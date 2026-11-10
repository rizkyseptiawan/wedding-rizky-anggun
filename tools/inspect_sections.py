with open("page_raw.html", "r", encoding="utf-8") as f:
    c = f.read()

import re

print("All section tags:")
sections = re.findall(r'<section[^>]*class=["\']([^"\']+)["\'][^>]*>', c)
for s in sections:
    print(" -", s)

print("\nAll main div ids:")
div_ids = re.findall(r'<div[^>]*id=["\']([^"\']+)["\'][^>]*>', c)
for d in div_ids[:30]:
    print(" -", d)

print("\nSearching for RSVP variable in scripts:")
m = re.findall(r'var RSVP = [^;]+;', c)
for v in m:
    print(v)

m_banks = re.findall(r'var BANK[A-Z_]* = [^;]+;', c)
for v in m_banks:
    print(v)
