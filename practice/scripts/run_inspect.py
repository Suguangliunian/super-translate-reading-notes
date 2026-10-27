
import sys, os
sys.path.insert(0, 'skill/engine')
from pdf_zh_translator.cli import main
rc = main(['inspect','materials/input.pdf','out/translated.pdf','--json-out','out/inspect.json'])
print('inspect_exit', rc)
