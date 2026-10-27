
import sys, os, time
sys.path.insert(0, 'skill/engine')
from pdf_zh_translator.cli import main

t0 = time.time()
rc = main(['translate','materials/input.pdf','out/translated.pdf',
 '--api-mode','openai-compatible','--api-url',os.environ['MODEL_API_BASE'],
 '--api-key-env','EVAL_LOCAL_KEY','--model',os.environ['MODEL_NAME'],
 '--preserve-graphics-text','--batch-size','12','--timeout','100',
 '--font-file','common-assets/NotoSansSC.ttf',
 '--cache-file','out/translation-cache.jsonl'])
print('translate_exit', rc, 'elapsed', time.time()-t0)
