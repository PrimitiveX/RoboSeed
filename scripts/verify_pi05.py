#!/usr/bin/env python3
"""Verify pi05 episode evidence, selected seeds, aggregate tables and source hashes offline."""
from collections import Counter
from pathlib import Path
import csv
import hashlib
import json
import math
import re
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/pi05'

def require(ok,msg):
    if not ok:raise ValueError(msg)

def read(name):
    with (DATA/name).open(newline='') as f:return list(csv.DictReader(f))

def close(a,b,msg):require(math.isclose(float(a),float(b),abs_tol=1e-8),msg)

def verify_pi05():
    meta=json.loads((DATA/'metadata.json').read_text())
    rows=[json.loads(x) for x in (DATA/'robotwin_episodes.jsonl').read_text().splitlines()]
    keys=[(r['task_config'],r['task_name'],r['episode']) for r in rows]
    require(len(rows)==len(set(keys))==10000,'pi05 RoboTwin episode uniqueness/coverage')
    require(sum(r['success'] for r in rows)==7246,'pi05 RoboTwin successes')
    require(all(isinstance(r['success'],bool) and r['steps']>=0 for r in rows),'pi05 invalid episode')
    require(Counter(r['result_source'] for r in rows)=={'original':6480,'retry':3520},'pi05 source selection')
    audit=json.loads((DATA/'robotwin_retry_audit.json').read_text())
    tasks=read('robotwin_task_results.csv')
    require(len(tasks)==100 and len({(r['scene'],r['task']) for r in tasks})==100,'pi05 task table')
    for r in tasks:
        group=[x for x in rows if (x['task_config'],x['task_name'])==(r['scene'],r['task'])]
        require(len(group)==100 and {x['episode'] for x in group}==set(range(100)),'pi05 per-task episode IDs')
        require(sum(x['success'] for x in group)==int(r['successes']),'pi05 task successes')
        close(r['success_rate_pct'],int(r['successes']),'pi05 task rate')
        counts=Counter(x['result_source'] for x in group)
        require(counts['original']==int(r['original_valid']) and counts['retry']==int(r['retry_selected']),'pi05 task retry count')
        key=r['scene']+'/'+r['task']; job=audit['jobs'][key]
        require(job['successes']==int(r['successes']) and job['evaluated']==100,'pi05 audit task')
        chosen=audit['retry_audit'][key]['selected_seed_by_episode']
        for x in group:
            if x['result_source']=='retry':require(int(chosen[str(x['episode'])])==x['seed'],'pi05 selected retry seed')
    for scene,s in [('demo_clean',3652),('demo_randomized',3594)]:
        group=[r for r in rows if r['task_config']==scene]
        require(len(group)==5000 and sum(r['success'] for r in group)==s,'pi05 scene aggregate')
    loss=read('robotwin_loss.csv')
    require([int(r['step']) for r in loss]==list(range(0,295471,10)),'pi05 loss interval')
    require(all(math.isfinite(float(r['loss'])) and float(r['loss'])>0 for r in loss),'pi05 loss values')
    close(loss[0]['loss'],.0721,'pi05 first loss');close(loss[-1]['loss'],.0012,'pi05 last loss')
    require(meta['robotwin']['updates']*meta['robotwin']['global_batch']==meta['robotwin']['sample_exposure']==4727600,'pi05 exposure')
    lib=[json.loads(x) for x in (DATA/'libero_episodes.jsonl').read_text().splitlines()]
    require(len(lib)==len({(r['suite'],r['task_id'],r['episode_idx']) for r in lib})==2000,'pi05 LIBERO uniqueness')
    require(all(r['status']=='completed' and r['seed']==7 for r in lib),'pi05 LIBERO completed/seed')
    require(sum(r['success'] for r in lib)==1944,'pi05 LIBERO successes')
    libtasks=read('libero_tasks.csv');require(len(libtasks)==40,'pi05 LIBERO tasks')
    for r in libtasks:
        group=[x for x in lib if x['suite']==r['suite'] and x['task_id']==int(r['task_id'])]
        require(len(group)==50 and {x['episode_idx'] for x in group}==set(range(50)),'pi05 LIBERO task coverage')
        require(sum(x['success'] for x in group)==int(r['successes']),'pi05 LIBERO task successes')
        close(r['success_rate_pct'],2*int(r['successes']),'pi05 LIBERO task rate')
    for r in read('libero_suite_results.csv'):
        group=[x for x in lib if x['suite']==r['suite']]
        require(len(group)==int(r['episodes'])==500 and sum(x['success'] for x in group)==int(r['local_successes']),'pi05 LIBERO suite')
        close(r['local_success_rate_pct'],100*sum(x['success'] for x in group)/len(group),'pi05 LIBERO suite rate')
    registry=meta['checkpoints']
    require(registry[0]['public_url'] is None and not meta['completion']['libero_local_post_train'],'pi05 completion/publication status')
    for entry in registry:
        require((ROOT/entry['record']).is_file() and (ROOT/entry['configuration']).is_file(),'pi05 record/config link')
    manifest=json.loads((DATA/'manifest.json').read_text())
    for path,info in manifest['files'].items():
        p=ROOT/path
        require(p.stat().st_size==info['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==info['sha256'],'pi05 hash mismatch: '+path)
    for info in json.loads((DATA/'provenance.json').read_text())['original_evidence'].values():
        require(info['bytes']>0 and re.fullmatch(r'[a-f0-9]{64}',info['sha256']),'pi05 original identity')
    print('pi05 evidence: 10,000 RoboTwin + 2,000 LIBERO unique episodes, retry seeds, all task/suite totals and 29,548 loss observations verified.')

if __name__=='__main__':verify_pi05()
