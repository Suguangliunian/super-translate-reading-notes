
import fitz, json, hashlib

# Verify translated.pdf opens and is valid
doc = fitz.open('out/translated.pdf')
print("translated.pdf pages:", doc.page_count, "rect:", doc[0].rect)

# Verify original unchanged (compare to full-paper.pdf page 4? just check input.pdf still opens)
odoc = fitz.open('materials/input.pdf')
print("input.pdf pages:", odoc.page_count, "rect:", odoc[0].rect)

# Verify audit json valid
a = json.load(open('out/reading-audit.json'))
print("audit paragraphs:", len(a['paragraphs']), "gaps:", len(a['gaps']))

# Verify checks json
c = json.load(open('out/checks.json'))
print("checks all pass:", all(v is True for v in c.values() if isinstance(v,bool)))

# Verify output.md exists and non-trivial
md = open('out/output.md').read()
print("output.md chars:", len(md))

# Confirm translated text contains Chinese and key numbers
t = doc[0].get_text()
print("has 5020:", '5020' in t, "has 4143:", '4143' in t, "has 图4:", '图4' in t, "has 表2:", '表2' in t)
