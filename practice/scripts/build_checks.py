
import fitz, json

# 1. Verifiable text export of translated PDF
doc = fitz.open('out/translated.pdf')
txt = doc[0].get_text()
open('out/translated-text.txt','w',encoding='utf-8').write(txt)

# Also export original for comparison
odoc = fitz.open('materials/input.pdf')
otxt = odoc[0].get_text()
open('out/original-text.txt','w',encoding='utf-8').write(otxt)

# 2. Machine-readable checks
checks = {}
checks['page_count_match'] = doc.page_count == odoc.page_count == 1
checks['page_size_match'] = (doc[0].rect.width == odoc[0].rect.width == 612.0 and
                             doc[0].rect.height == odoc[0].rect.height == 792.0)
checks['image_preserved'] = len(doc[0].get_images(full=True)) == 1

# Check all numeric values from tables preserved in translated text
import re
def nums(s):
    return set(re.findall(r'\d+(?:\.\d+)?%?', s))
onums = nums(otxt)
tnums = nums(txt)
checks['table_numbers_preserved'] = onums <= tnums  # all original numbers still present

# Check key numbers
for key in ['44.4','77.1','69.5','77.9','68.7','43.2','24.7','63.8','11.6','26.1','3.9','16.0',
            '55.6','80.7','72.9','80.8','75.2','48.8','29.0','69.6','18.9','35.4','6.0','34.3',
            '36.9','62.9','62.3','72.8','59.4','34.5','11.0','34.9','31.1','52.5','5.2','20.8',
            '60.1','81.3','75.3','83.0','80.0','55.5','28.8','69.9','30.5','47.5','13.1','52.2',
            '1047','7.2','1031','6.84','1012','6.65','1041','6.57','985','6.27','997','6.17','914','4.53',
            '5020','4143']:
    if key not in txt:
        checks.setdefault('missing_numbers', []).append(key)
checks['all_key_numbers_present'] = 'missing_numbers' not in checks

# Check Chinese present (prose translated)
cjk = sum(1 for c in txt if '\u4e00' <= c <= '\u9fff')
checks['chinese_chars_count'] = cjk
checks['prose_translated'] = cjk > 200

# Check no leftover English prose sentences (only table/figure labels should remain)
# English words that should NOT remain as full sentences
leftover_en = re.findall(r'\b[A-Z][a-z]+ [a-z]+ [a-z]+ [a-z]+\b', txt)
checks['leftover_english_phrases'] = leftover_en

json.dump(checks, open('out/checks.json','w'), ensure_ascii=False, indent=2)
print(json.dumps(checks, ensure_ascii=False, indent=2))
