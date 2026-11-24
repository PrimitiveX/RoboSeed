#!/usr/bin/env python3
"""Refresh pi05 evidence/report identities; run the verifier after reviewing changes."""
from pathlib import Path
import hashlib
import json
ROOT = Path(__file__).resolve().parents[1]

def info(p):
    return {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def main():
    paths = list((ROOT/'data/pi05').glob('*')) + list((ROOT/'configs/pi05').glob('*'))
    for n in ('18_pi05_architecture','19_pi05_experiments'):
        paths += list((ROOT/'docs/figure/results').glob(n+'.*'))
    files={p.relative_to(ROOT).as_posix():info(p) for p in sorted(paths) if p.is_file() and p.name!='manifest.json'}
    (ROOT/'data/pi05/manifest.json').write_text(json.dumps({'as_of':'2026-11-24','scope':'Packaged public pi05 evidence, recorded configs and figure assets; authoritative LaTeX source remains in the separate article project. Original source hashes are in provenance.json.','files':files},indent=2)+'\n')
    path=ROOT/'data/report_refresh.json'; meta=json.loads(path.read_text())
    meta.setdefault('previous_report_sha256',meta['report_sha256'])
    meta.update(report_updated='2026-11-24',report_sha256=info(ROOT/'docs/report/RoboSeed.pdf')['sha256'])
    meta['pi05_addition']={'metadata':'pi05/metadata.json','manifest':'pi05/manifest.json','existing_assessment_profiles':12,'new_experiments_outside_assessment':2,'article_source_project':'Separately managed roboseed/report; not duplicated inside this Git repository'}
    path.write_text(json.dumps(meta,indent=2)+'\n')

if __name__=='__main__':main()
