#!/usr/bin/env python3
"""Import public pi05 artifacts from RoboSeed's separately maintained article project."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
ROOT=Path(__file__).resolve().parents[1]
PUBLIC_DATA=['README.md','metadata.json','provenance.json','report_text.md','robotwin_episodes.jsonl','robotwin_retry_audit.json','robotwin_task_results.csv','robotwin_loss.csv','libero_episodes.jsonl','libero_tasks.csv','libero_suite_results.csv']

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--article-root',type=Path,default=ROOT.parent/'report')
 args=p.parse_args(); article=args.article_root.resolve()
 manifest=json.loads((article/'data/pi05/article_manifest.json').read_text())
 # Validate all article source identities before copying public material.
 for name,info in manifest['files'].items():
  q=article/name
  if q.stat().st_size!=info['bytes'] or hashlib.sha256(q.read_bytes()).hexdigest()!=info['sha256']:
   raise SystemExit('Article source changed; refresh and validate its manifest first: '+name)
 q=article/'RoboSeed.pdf'
 if hashlib.sha256(q.read_bytes()).hexdigest()!=manifest['report']['sha256']:
  raise SystemExit('Article report PDF differs from its verified manifest')
 out=ROOT/'data/pi05';out.mkdir(exist_ok=True)
 for name in PUBLIC_DATA:
  if name=='README.md':continue # Git companion documentation has different relative links.
  shutil.copyfile(article/'data/pi05'/name,out/name)
 text=(out/'report_text.md').read_text().replace('../../figures/','../../docs/figure/results/')
 (out/'report_text.md').write_text(text)
 for q in (article/'data/pi05/configs').glob('*'):
  if q.is_file():
   target=ROOT/'configs/pi05'/q.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(q,target)
 for stem in ['18_pi05_architecture','19_pi05_experiments']:
  for ext in ['pdf','svg','png']:shutil.copyfile(article/'figures'/f'{stem}.{ext}',ROOT/'docs/figure/results'/f'{stem}.{ext}')
 shutil.copyfile(article/'RoboSeed.pdf',ROOT/'docs/report/RoboSeed.pdf')
 print('Imported public pi05 evidence/configs/figures and complete PDF; no LaTeX project, local publication plans or weights copied into Git.')
if __name__=='__main__':main()
