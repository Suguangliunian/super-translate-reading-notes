"""Recheck the saved paper/translation. No model requests, no model benchmark rerun."""
from pathlib import Path
import csv
import hashlib
import json
import re
import sys

import fitz
import numpy as np
from PIL import Image, ImageDraw
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'verification'
DEST.mkdir(exist_ok=True)
REGIONS = {'figure4': (106, 75, 506, 198),
           'table2': (106, 260, 506, 324),
           'table3': (313, 531, 503, 633)}
METRICS = ['MMLU', 'HellaSwag', 'WinoG', 'PIQA', 'Arc-e', 'Arc-c',
           'NQ', 'TriviaQA', 'HumanEval', 'MBPP', 'MATH', 'GSM8K']

def image(page, rect=None):
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(rect) if rect else None,
                         colorspace=fitz.csRGB, alpha=False)
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)

def table_rows(page):
    words = page.get_text('words', clip=fitz.Rect(REGIONS['table2']))
    # Row positions come from the provided original page. Percent tokens are
    # sorted by x, not by the potentially scrambled PDF text-reading order.
    rows = {}
    for label, y in [('Llama2-13B', 287.4), ('Mistral7B', 313.7)]:
        matches = sorted([(w[0], w[4]) for w in words
                          if abs(w[1] - y) < 1 and re.fullmatch(r'\d+\.\d+%', w[4])])
        if len(matches) != 12:
            raise ValueError(f'Expected 12 numeric columns for {label}, got {len(matches)}')
        rows[label] = [float(word[:-1]) for _, word in matches]
    return rows

original = fitz.open(ROOT / 'paper/input.pdf')
translated = fitz.open(ROOT / 'practice/out/translated.pdf')
assert len(original) == len(translated) == 1
assert original[0].rect == translated[0].rect
assert original[0].get_text().strip() and translated[0].get_text().strip()
checks = []
for name, rect in REGIONS.items():
    a, b = image(original[0], rect), image(translated[0], rect)
    x, y = np.array(a), np.array(b)
    assert x.shape == y.shape
    delta = np.abs(x.astype(float) - y.astype(float)) / 255
    checks.append({'region': name, 'pdf_page_index': 0, 'rect_pt': rect,
                   'mean_absolute_rgb_difference_0_to_1': float(delta.mean()),
                   'changed_pixel_fraction': float(np.any(x != y, axis=2).mean()),
                   'exact_pixel_equal': bool(np.array_equal(x, y))})
    if name == 'table2':
        a.save(DEST / 'table2-original.png')

rows = table_rows(original[0])
assert table_rows(translated[0]) == rows, 'Numeric text in protected table differs'
with (ROOT / 'paper/table2-checked.csv').open(encoding='utf8', newline='') as f:
    hand_checked = list(csv.DictReader(f))
assert [r['metric'] for r in hand_checked] == METRICS
for r, metric, a, b in zip(hand_checked, METRICS, rows['Llama2-13B'], rows['Mistral7B']):
    assert float(r['llama2_13b']) == a and float(r['mistral_7b']) == b, metric
deltas = [round(b - a, 1) for a, b in zip(rows['Llama2-13B'], rows['Mistral7B'])]
comparison = [{'metric': metric, 'llama2_13b': a, 'mistral_7b': b, 'delta_pp': d}
              for metric, a, b, d in zip(METRICS, rows['Llama2-13B'], rows['Mistral7B'], deltas)]
counterexamples = [r for r in comparison if r['delta_pp'] <= 0]
ai_report = (ROOT / 'practice/out/output.md').read_text('utf8')
result = {
    'scope': 'Local artifact and table-consistency checks for one saved Mistral page; not a new inference or benchmark run.',
    'paper_original_page': 4, 'page_size_pt': list(original[0].rect),
    'pages_match': True, 'regions': checks,
    'table_extraction_matches_manually_checked_csv': True,
    'table_values_match_translated_pdf': True,
    'comparison': comparison, 'strictly_higher_metrics': sum(x > 0 for x in deltas),
    'compared_metrics': len(METRICS), 'all_metrics_superior': not counterexamples,
    'counterexamples': counterexamples,
    'ai_report_repeats_all_metrics_claim': '在所有指标上优于 Llama 2 13B' in ai_report,
    'ai_report_mentions_nq_29_0': '29.0' in ai_report,
    'interpretation': 'Layout preservation passed for the three fixed crops. The Table 2 universal superiority claim is contradicted by NQ 28.8 < 29.0. These checks do not validate all translation semantics, statistical significance, or underlying benchmark experiments.',
    'sha256': {str(p.relative_to(ROOT)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in [ROOT/'paper/input.pdf', ROOT/'practice/out/translated.pdf', ROOT/'practice/out/output.md']},
}
(DEST / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

# Reader-facing original/translated page image; exact crops are measured above.
a, b = image(original[0]), image(translated[0])
canvas = Image.new('RGB', (a.width + b.width, max(a.height, b.height) + 44), 'white')
canvas.paste(a, (0, 44)); canvas.paste(b, (a.width, 44))
draw = ImageDraw.Draw(canvas)
draw.text((20, 12), 'Original Mistral 7B v1, PDF page 4', fill='black')
draw.text((a.width + 20, 12), 'Saved SuperTranslate + DeepSeek Pro output', fill='black')
canvas.save(DEST / 'page-comparison.png')

fig, ax = plt.subplots(figsize=(9, 5.3), layout='constrained')
positions = np.arange(len(METRICS))
ax.barh(positions, deltas, color=['#b32940' if d < 0 else '#326a8c' for d in deltas])
ax.set_yticks(positions, METRICS); ax.invert_yaxis(); ax.axvline(0, color='#333333', linewidth=.8)
ax.set_xlim(-2, max(deltas) + 3)
for i, d in enumerate(deltas):
    ax.text(d + .2 if d >= 0 else d - .2, i, f'{d:+.1f}', va='center',
            ha='left' if d >= 0 else 'right', fontsize=10)
ax.set_title('Mistral 7B minus Llama 2 13B: 11 of 12 metrics are higher')
ax.set_xlabel('Score difference (percentage points); source: Mistral 7B v1, Table 2')
ax.spines[['top', 'right']].set_visible(False)
fig.savefig(DEST / 'table2-differences.png', dpi=180)
plt.close(fig)
assert all(r['exact_pixel_equal'] for r in checks)
assert counterexamples == [{'metric': 'NQ', 'llama2_13b': 29.0, 'mistral_7b': 28.8, 'delta_pp': -0.2}]
print(json.dumps({'regions_identical': len(checks), 'higher': result['strictly_higher_metrics'],
                  'total': len(METRICS), 'counterexamples': counterexamples,
                  'output': str(DEST / 'result.json')}, ensure_ascii=False))
