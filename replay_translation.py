"""Replay recorded translations through the pinned engine; never calls a model."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import sys
import time
import fitz
import numpy as np

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--engine', type=Path, required=True)
args = p.parse_args()
root = Path(__file__).resolve().parent
engine = args.engine.resolve()
if not (engine / 'pdf_zh_translator/cli.py').is_file():
    raise SystemExit('Pass the root of the pinned upstream checkout.')
dest = root / 'rerun'
dest.mkdir(exist_ok=True)
cache = dest / 'translation-cache.jsonl'
shutil.copyfile(root / 'practice/out/translation-cache.jsonl', cache)
sys.path.insert(0, str(engine))
from pdf_zh_translator.cli import main
started = time.monotonic()
rc = main(['translate', str(root/'paper/input.pdf'), str(dest/'translated.pdf'),
           '--api-mode', 'cache-only', '--cache-segments', '--preserve-graphics-text',
           '--batch-size', '12', '--timeout', '100',
           '--font-file', str(root/'assets/NotoSansSC.ttf'), '--cache-file', str(cache)])
if rc:
    raise SystemExit(rc)
a = fitz.open(root / 'practice/out/translated.pdf')
b = fitz.open(dest / 'translated.pdf')
assert len(a) == len(b) == 1 and a[0].rect == b[0].rect
pa = a[0].get_pixmap(matrix=fitz.Matrix(2, 2), colorspace=fitz.csRGB, alpha=False)
pb = b[0].get_pixmap(matrix=fitz.Matrix(2, 2), colorspace=fitz.csRGB, alpha=False)
equal = pa.width == pb.width and pa.height == pb.height and pa.samples == pb.samples
report = {'operation': 'cache-only layout replay; no inference and no new AI reading',
          'upstream_commit_required': 'f16a641b9c7be155938d6b0e047b24e944dd4668',
          'translation_exit': rc, 'pages_match': True,
          'full_page_pixels_equal_at_2x': equal,
          'elapsed_seconds': round(time.monotonic() - started, 3),
          'note': 'PDF binary metadata may differ; compare rendered pages, not output file hashes.'}
(root/'verification/replay-result.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
print(json.dumps(report, ensure_ascii=False))
assert equal, 'Saved and replayed full-page pixels differ; inspect before claiming a match.'
