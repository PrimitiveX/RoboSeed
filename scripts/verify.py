#!/usr/bin/env python3
"""Check published aggregates, evidence selections, generated pages, and local links."""
from pathlib import Path
from collections import Counter, defaultdict
from urllib.parse import unquote, urlsplit
import argparse
import csv
import hashlib
import html
import json
import math
import re
import xml.etree.ElementTree as ET

from generate_docs import ROOT, build, slug


def require(condition, message):
    if not condition:
        raise ValueError(message)


def close(a, b, message):
    require(math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-8), message)


def read(name):
    with (ROOT / 'data' / name).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def read_json(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))


def unique(rows, keys, label):
    ids = [tuple(r[k] for k in keys) for r in rows]
    require(len(ids) == len(set(ids)), f'{label}: duplicate {keys}')


def totals(rows, denominator='episodes'):
    return sum(int(r['success']) for r in rows), sum(int(r[denominator]) for r in rows)


def rates(rows, denominator='episodes'):
    for r in rows:
        s = int(r['success']); n = int(r[denominator])
        require(0 <= s <= n and n > 0, f'Invalid counts: {r}')
        if 'success_rate_pct' in r:
            close(r['success_rate_pct'], 100 * s / n, f'Rate disagrees: {r}')


def verify_results():
    summary = read('robotwin_summary.csv'); tasks = read('robotwin_tasks.csv'); pending = read('robotwin_training_only.csv')
    unique(summary, ['backbone'], 'RoboTwin summary'); unique(tasks, ['backbone', 'suite', 'task'], 'RoboTwin tasks'); rates(tasks)
    require(len(tasks) == len(summary) * 100, 'RoboTwin: expected 50 tasks in each of two scenes per completed backbone')
    for r in summary:
        for scene, key in [('Clean', 'clean'), ('Randomized', 'randomized')]:
            group = [t for t in tasks if t['backbone'] == r['backbone'] and t['suite'] == scene]
            s, n = totals(group)
            require(len(group) == 50 and all(int(t['episodes']) == 100 for t in group), 'RoboTwin task denominator')
            require(s == int(r[key + '_success']) and n == int(r['episodes_per_scene']), 'RoboTwin aggregate counts')
            close(r[key + '_pct'], 100 * s / n, 'RoboTwin aggregate rate')
        close(r['avg_pct'], (float(r['clean_pct']) + float(r['randomized_pct'])) / 2, 'RoboTwin scene average')
        close(r['gpu_hours'], 4 * float(r['train_hours']), 'RoboTwin GPU-hours')
        close(r['samples_per_s'], 150000 * 64 / (float(r['train_hours']) * 3600), 'RoboTwin throughput')
        path = ROOT / 'docs/experiments/abot-m0/robotwin' / (slug(r['backbone']) + '-task-results.csv')
        with path.open(newline='') as f:
            old = list(csv.DictReader(f))
        for t in old:
            for scene, key in [('Clean', 'clean'), ('Randomized', 'randomized')]:
                actual = next(x for x in tasks if x['backbone'] == r['backbone'] and x['suite'] == scene and x['task'] == t['task'])
                close(t[key + '_success_rate'], int(actual['success']) / int(actual['episodes']), 'Compatibility CSV rate')
    completed = {r['backbone'] for r in summary}; waiting = {r['backbone'] for r in pending}
    require(not completed & waiting, 'Training-only model appears in completed results')
    loss = read('robotwin_loss.csv'); unique(loss, ['backbone', 'step'], 'RoboTwin loss')
    require({r['backbone'] for r in loss} == completed | waiting, 'Loss coverage differs from training coverage')
    for r in summary + pending:
        group = [t for t in loss if t['backbone'] == r['backbone']]
        steps = [int(t['step']) for t in group]
        require(steps == sorted(steps) and steps[-1] == 150000, 'RoboTwin final training step')
        require(all(math.isfinite(float(t['action_dit_loss'])) and float(t['action_dit_loss']) > 0 for t in group), 'Invalid loss observation')
        if r in summary:
            require(len(group) == int(r['loss_log_points']), 'Loss observation count')

    libero = read('libero_tasks.csv'); rc = read('robocasa_tasks.csv'); lp = read('liberoplus_tasks.csv')
    unique(libero, ['suite', 'task'], 'LIBERO'); unique(rc, ['task'], 'RoboCasa'); unique(lp, ['suite', 'task_id'], 'LIBERO-plus')
    for rows in [libero, rc, lp]:
        rates(rows)
    require(len(libero) == 40 and totals(libero) == (1935, 2000), 'LIBERO counts')
    require(len(rc) == 24 and totals(rc) == (574, 1200), 'RoboCasa counts')
    require(len(lp) == 10030 and totals(lp) == (8027, 10030), 'LIBERO-plus counts')
    for name, key in [('liberoplus_suite.csv', 'suite'), ('liberoplus_category.csv', 'category')]:
        rows = read(name); rates(rows)
        require(totals(rows) == totals(lp), 'LIBERO-plus aggregate denominator')
        for r in rows:
            require(totals([t for t in lp if t[key] == r[key]]) == (int(r['success']), int(r['episodes'])), 'LIBERO-plus grouping mismatch')
    duplicates = read_json('liberoplus_duplicates.json')
    require(len(duplicates) == 101 and sum(bool(d['conflicting']) for d in duplicates) == 3, 'LIBERO-plus duplicate audit')
    for d in duplicates:
        require(d['chosen'] == max(d['alternatives'], key=lambda r: r['mtime']), 'LIBERO-plus latest-mtime selection')
        chosen = next(t for t in lp if t['suite'] == d['suite'] and int(t['task_id']) == int(d['task_id']))
        require(int(chosen['success']) == int(d['chosen']['success']), 'Duplicate choice differs from result')

    videos = read('video_index.csv')
    for benchmark, rows in [('LIBERO', libero), ('RoboCasa', rc)]:
        selected = [v for v in videos if v['benchmark'] == benchmark]
        unique(selected, ['suite', 'task', 'episode'], benchmark + ' video evidence')
        for r in rows:
            task = r['task'] if benchmark == 'LIBERO' else 'gr1_unified_' + r['task'] + '_GR1ArmsAndWaistFourierHands_Env'
            group = [v for v in selected if v['task'] == task and (benchmark != 'LIBERO' or v['suite'] == r['suite'])]
            require((sum(int(v['success']) for v in group), len(group)) == (int(r['success']), int(r['episodes'])), benchmark + ' video counts')
            if benchmark == 'LIBERO':
                require({int(v['episode']) for v in group} == set(range(50)), 'LIBERO episode IDs')
    selected_lp = defaultdict(list)
    for v in videos:
        if v['benchmark'] == 'LIBERO-plus':
            selected_lp[v['suite'], int(v['task'])].append(v)
    audit = {(d['suite'], int(d['task_id'])): d for d in duplicates}
    for r in lp:
        key = (r['suite'], int(r['task_id'])); group = selected_lp[key]
        if key in audit:
            group = [v for v in group if v['path'] == audit[key]['chosen']['path']]
        require(len(group) == 1 and int(group[0]['success']) == int(r['success']), 'LIBERO-plus selected video verdict')

    cs = read('calvin_summary.csv')[0]; chain = read('calvin_chain.csv'); ct = read('calvin_tasks.csv')
    rates(chain, 'sequences'); rates(ct, 'attempts'); unique(ct, ['task'], 'CALVIN task types')
    require(len(ct) == 34 and totals(ct, 'attempts') == (3625, 4054), 'CALVIN conditional counts')
    require([int(r['success']) for r in chain] == [889, 798, 721, 646, 571], 'CALVIN prefix counts')
    require(all(int(r['sequences']) == 1000 for r in chain), 'CALVIN sequence denominators')
    close(sum(int(r['success']) for r in chain) / int(cs['sequences']), cs['avg_seq_len'], 'CALVIN mean length')
    require(sum(int(r['success']) for r in chain) == int(cs['successful_subtasks']), 'CALVIN chain/task aggregate agreement')
    close(cs['gpu_hours'], 4 * float(cs['train_hours']), 'CALVIN GPU-hours')
    families = read('calvin_families.csv'); rates(families, 'attempts')
    horizontal = [r for r in ct if r['task'].startswith('push_') and r['task'].endswith(('_left', '_right'))]
    for f in families:
        group = horizontal if f['family'] == 'Horizontal push' else [r for r in horizontal if r['task'].endswith('_left')] if f['family'] == 'Push left' else [r for r in horizontal if r['task'].endswith('_right')] if f['family'] == 'Push right' else [r for r in ct if r not in horizontal]
        require(len(group) == int(f['tasks']) and totals(group, 'attempts') == (int(f['success']), int(f['attempts'])), 'CALVIN failure-family counts')
    audit = read_json('calvin_audit.json'); source = read_json('calvin_results_source.json')
    require([r['key'] for r in audit['records']] == ['0', '0'], 'CALVIN duplicate keys must remain explicit')
    require(audit['records'][-1]['record'] == source['0'], 'CALVIN final duplicate occurrence')
    for r in ct:
        require(source['0']['task_info'][r['task']] == {'success': int(r['success']), 'total': int(r['attempts'])}, 'CALVIN source task counts')
    closs = read('calvin_loss.csv')
    require(len(closs) == 340 and [int(r['step']) for r in closs] == list(range(100, 34001, 100)), 'CALVIN final-run loss coverage')
    close(closs[-1]['action_dit_loss'], cs['final_action_dit_loss'], 'CALVIN final logged loss')
    require(audit['training_log']['raw_observations'] == len(closs) + audit['training_log']['discarded_preliminary_observations'], 'CALVIN preliminary loss audit')

    registry = read_json('checkpoints.json')['checkpoints']
    require(len(registry) == 9, 'Expected nine recorded checkpoint mappings')
    unique(registry, ['benchmark', 'backbone'], 'Checkpoint registry')
    original = {(r['benchmark'], r['backbone']): r for r in read_json('source_manifest.json')['canonical_models']}
    for r in registry:
        require(r['checkpoint_bytes'] == original[r['benchmark'], r['backbone']]['checkpoint_bytes'], 'Checkpoint byte count')
        for key in ['configuration', 'record']:
            require((ROOT / r[key]).is_file(), 'Missing checkpoint metadata link')
        config = (ROOT / r['configuration']).read_text()
        require(int(re.search(r'^\s*max_train_steps:\s*(\d+)', config, re.M)[1]) == r['updates'], 'Configuration update count')
    verify_refresh()
    print('Counts and evidence: ABot RoboTwin 60,000 episodes; LIBERO 2,000; LIBERO-plus 10,030; RoboCasa 1,200; CALVIN 1,000 chains.')


def verify_refresh():
    tasks = read('extension_tasks.csv'); units = read_json('extension_units.json')
    assessment = read_json('assessment.json')
    require(len(tasks) == 1000 and len(units) == 12, 'Report extension coverage')
    unique(tasks, ['unit', 'scene', 'task'], 'Report extension'); rates(tasks)
    require({r['unit'] for r in tasks} == {u['id'] for u in units}, 'Extension unit mapping')
    profiles = {u['id']: u for u in assessment['units']}
    abot = {(r['backbone'], r['suite'], r['task']): r for r in read('robotwin_tasks.csv')}
    for u in units:
        observed = [r for r in tasks if r['unit'] == u['id']]
        scenes = {'Clean', 'Randomized'} if u['method'] in {'ABot-M0', 'OpenWAM'} else {'Clean'}
        require({r['scene'] for r in observed} == scenes, 'Unexpected scene coverage')
        for scene in scenes:
            group = [r for r in observed if r['scene'] == scene]
            require(len(group) == 50 and all(int(r['episodes']) == (5 if u['method'] == 'LiLa-WAM' else 100) for r in group), 'Extension task denominators')
            result = profiles[u['id']]['scenes'][scene]
            require(totals(group) == (result['success'], result['episodes']), 'Assessment disagrees with task counts')
            if u['method'] == 'ABot-M0':
                for r in group:
                    original = abot[u['label'].removeprefix('ABot '), scene, r['task']]
                    require(int(r['success']) == int(original['success']), 'ABot extension/canonical task mismatch')
        scores = profiles[u['id']]['scores']
        if scenes == {'Clean', 'Randomized'}:
            close(scores['P'], sum(profiles[u['id']]['scenes'][s]['pct'] for s in scenes)/2, 'Two-scene assessment P')
        else:
            require(scores['P'] is None, 'Missing scene must not receive two-scene P')
        require(scores['D'] is None and all(v is None for v in profiles[u['id']]['total'].values()), 'Missing deployment measurements must withhold composites')
    for name, count in [('ling_training_observations.csv', 50000), ('openwam_training_observations.csv', 80000), ('lila_stage1_training_observations.csv', 23643), ('lila_stage2_training_observations.csv', 7881)]:
        require(len(read(name)) == count, 'Native loss selection count: ' + name)
    for name, expected in [('harness_original_all50_tasks.csv', 411), ('harness_w6_tasks.csv', 408), ('harness_w16_tasks.csv', 401)]:
        group = read(name); unique(group, ['task'], name)
        require(len(group) == 50 and totals(group) == (expected, 500), 'Full-task harness counts')
    fresh = read('harness_refresh.csv')
    matched = [r for r in fresh if r['run'].startswith('px_4gpu_batch_compare_')]
    require(len(matched) == 3 and len({r['episode_inputs_sha256'] for r in matched}) == 1, 'Matched-input systems comparison')
    for r in fresh:
        close(r['gpu_hours'], int(r['gpus'])*float(r['wall_seconds'])/3600, 'Harness rollout GPU-hours')
        require(float(r['end_to_end_seconds']) >= float(r['wall_seconds']), 'Startup-inclusive timing scope')
    packages = read_json('modelscope_packages.json')['packages']
    require(len(packages) == 17, 'ModelScope package coverage')
    unique(packages, ['package_id'], 'ModelScope packages')
    require(Counter(p['status'] for p in packages) == {'evaluated': 15, 'training_prefix_no_rollout': 2}, 'Model package status coverage')
    for p in packages:
        require(p['public_url'] == 'https://www.modelscope.cn/models/InPeerReview/RoboSeed/tree/master/' + p['path'], 'ModelScope folder URL')
        require(p['weight_files'], 'Package without observed weights')
        for f in p['weight_files']:
            require(f['path'].startswith(p['path'] + '/') and f['bytes'] > 0 and re.fullmatch('[0-9a-f]{64}', f['sha256']), 'Invalid remote weight metadata')
    for r in read_json('checkpoints.json')['checkpoints']:
        pkg = next(p for p in packages if p['public_url'] == r['public_url'])
        require(r['revision'] == 'master' and r['evaluation_status'] == 'complete', 'Stale ABot release metadata')
        require(sum(f['bytes'] for f in pkg['weight_files']) == r['checkpoint_bytes'], 'ModelScope/record weight size mismatch')
    require(hashlib.sha256((ROOT / 'docs/report/RoboSeed.pdf').read_bytes()).hexdigest() == read_json('report_refresh.json')['report_sha256'], 'Report PDF differs from refresh source')
    print('Report refresh: 1,000 task rows, 12 checkpoint profiles, native losses, harness evidence and 17 published package mappings checked.')


def heading_ids(text):
    counts = Counter(); result = set()
    for label in re.findall(r'^#{1,6}\s+(.+)$', text, re.M):
        label = re.sub(r'<[^>]*>', '', label)
        label = re.sub(r'[^\w\- ]', '', html.unescape(label).lower()).replace(' ', '-')
        suffix = '' if counts[label] == 0 else '-' + str(counts[label])
        result.add(label + suffix); counts[label] += 1
    return result


def verify_documents(allow_missing_manifest=False):
    generated = build()
    for name, text in generated.items():
        require((ROOT / name).read_text(encoding='utf-8') == text, f'Generated content stale: {name}')
    files = [ROOT / 'README.md', ROOT / 'CONTRIBUTING.md', ROOT / 'CHANGELOG.md'] + list((ROOT / 'docs').rglob('*.md')) + list((ROOT / 'data').glob('*.md')) + list((ROOT / 'configs').glob('*.md'))
    links = 0
    for path in files:
        text = path.read_text(encoding='utf-8')
        require(not re.search(r'\bS[12]\b|<ORG>|待补充|TODO', text), f'Unresolved old label/placeholder: {path.relative_to(ROOT)}')
        targets = re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text) + re.findall(r'(?:href|src)="([^"]+)"', text)
        for target in targets:
            parsed = urlsplit(html.unescape(target.strip().strip('<>')))
            if parsed.scheme or parsed.netloc:
                continue
            dest = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if allow_missing_manifest and dest == ROOT / 'data/release_manifest.json' and not dest.exists():
                links += 1
                continue
            require(dest.is_relative_to(ROOT) and dest.exists(), f'Broken local link in {path.relative_to(ROOT)}: {target}')
            if parsed.fragment and dest.suffix == '.md':
                require(unquote(parsed.fragment) in heading_ids(dest.read_text(encoding='utf-8')), f'Broken heading link: {target}')
            links += 1
    for path in (ROOT / 'docs/figure').rglob('*.svg'):
        ET.parse(path)
    print(f'Documentation: {len(files)} Markdown files, {links} local links, generated content and SVG syntax checked.')


def inventory():
    paths = list((ROOT / 'data').glob('*')) + list((ROOT / 'configs/abot-m0').glob('*.yaml')) + list((ROOT / 'docs/report').glob('*.pdf'))
    return {p.relative_to(ROOT).as_posix(): {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(paths) if p.is_file() and p.name != 'release_manifest.json'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-manifest', action='store_true', help='Refresh hashes after counts, evidence and links pass.')
    args = parser.parse_args()
    verify_results(); verify_documents(allow_missing_manifest=args.write_manifest)
    path = ROOT / 'data/release_manifest.json'
    current = inventory()
    if args.write_manifest:
        path.write_text(json.dumps({'as_of': read_json('source_manifest.json')['snapshot_date'], 'scope': 'Packaged results, audits, recorded configs, and report PDF. Original source hashes are in source_manifest.json.', 'files': current}, indent=2) + '\n', encoding='utf-8')
        print(f'Wrote release hash inventory: {len(current)} files.')
    require(path.exists(), 'Missing release_manifest.json; use --write-manifest after reviewing the source changes')
    require(json.loads(path.read_text())['files'] == current, 'Packaged hashes differ from release_manifest.json')
    print(f'Artifact hashes: {len(current)} packaged files checked. All checks passed.')


if __name__ == '__main__':
    main()
