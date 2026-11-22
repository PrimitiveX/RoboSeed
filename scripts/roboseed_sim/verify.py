#!/usr/bin/env python3
"""Verify published counts, paired inputs, scaling summaries and replay outcomes."""
from collections import defaultdict
from pathlib import Path
import csv
import json
import math

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data/roboseed_sim'


def require(condition, message):
    if not condition:
        raise ValueError('RoboSeed-Sim: ' + message)


def close(a, b, message):
    require(math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-7), message)


def read(name):
    return json.loads((DATA / name).read_text())


def rows(name):
    with (DATA / name).open() as f:
        return list(csv.DictReader(f))


def verify():
    full = rows('full_task_results.csv')
    episodes = rows('full_episode_results.csv')
    require(len(full) == 100 and len(episodes) == 1600, 'full-task coverage')
    require(len({(r['scene'], r['task'], r['seed']) for r in episodes}) == 1600,
            'duplicate full-task episodes')
    require(all(r['instruction'].strip() for r in episodes), 'missing saved full-task instruction')
    for scene, expected, seconds in [('clean', 657, 14851.97), ('randomized', 648, 17360.90)]:
        selected = [r for r in full if r['scene'] == scene]
        require(len(selected) == 50 and all(int(r['episodes']) == 16 for r in selected), 'task denominators')
        require(sum(int(r['success']) for r in selected) == expected, 'full-task successes')
        close(sum(float(r['process_seconds']) for r in selected), seconds, 'full-task process time')
        for r in selected:
            group = [e for e in episodes if e['scene'] == scene and e['task'] == r['task']]
            require(len(group) == 16 and sum(int(e['success']) for e in group) == int(r['success']), 'task/episode mismatch')

    paired = rows('historical_paired_results.csv')
    profiles = read('historical_task_profiles.json')
    require(len(paired) == 800 and len(profiles) == 50, 'historical pairing coverage')
    for key, expected in [('cpu_n1', 681), ('gpu_n1', 657), ('gpu_n16', 657)]:
        require(sum(int(r[key]) for r in paired) == expected, 'historical paired totals')
        for task in profiles:
            require(sum(int(r[key]) for r in paired if r['task'] == task['task']) == task[key], 'profile counts')
    require(sum(r['gpu_n1'] != r['gpu_n16'] for r in paired) == 84, 'GPU disagreement count')
    require(sum(r['cpu_n1'] != r['gpu_n1'] for r in paired) == 100, 'CPU/GPU disagreement count')
    for task in profiles:
        require(sum(r['gpu_n1'] != r['gpu_n16'] for r in paired if r['task'] == task['task']) == task['gpu_disagreements'], 'profile disagreement')

    small = read('small_system_compare.json')
    small_pairs = rows('small_paired_episodes.csv')
    require(len(small_pairs) == 96, 'small paired coverage')
    for scene, original, migrated in [('clean', 41, 37), ('randomized', 36, 37)]:
        tasks = small['results'][scene]
        require(sum(r['original']['success'] for r in tasks.values()) == original, 'small original count')
        require(sum(r['batch']['success'] for r in tasks.values()) == migrated, 'small migrated count')
        for task, r in tasks.items():
            group = [e for e in small_pairs if e['scene'] == scene and e['task'] == task]
            require([int(e['seed']) for e in group] == r['seeds'], 'small seed pairing')
            for system, column in [('original', 'original_success'), ('batch', 'migrated_success')]:
                require(sum(int(e[column]) for e in group) == r[system]['success'], 'small paired success count')

    runs = read('scaling_runs.json')
    by_id = {r['run_id']: r for r in runs}
    require(len(by_id) == len(runs) == 48, 'scaling run count')
    groups = defaultdict(list)
    gpu_samples = defaultdict(list)
    for sample in rows('gpu_samples.csv'):
        require(sample['run_id'] in by_id, 'unknown GPU sample run')
        gpu_samples[sample['run_id']].append(int(sample['memory_mib']))
    for r in runs:
        require(len(r['seeds']) == len(r['instructions']) == len(r['successes']) == r['n'], 'scaling run denominator')
        require(sum(r['successes']) == r['success'], 'scaling run successes')
        require(r['direct_substeps'] == 17 and r['settle_steps'] == 2500, 'scaling control settings')
        groups[r['task'], r['n']].append(r)
    total_mib = read('protocol.json')['gpu_total_mib']
    for row in rows('scaling_summary.csv'):
        task, n = row['task'], int(row['n'])
        selected = groups[task, n]
        reference = groups[task, 16]
        seeds = [seed for r in selected for seed in r['seeds']]
        inst = [text for r in selected for text in r['instructions']]
        outcomes = [v for r in selected for v in r['successes']]
        ref_seeds = [seed for r in reference for seed in r['seeds']]
        ref_inst = [text for r in reference for text in r['instructions']]
        require(seeds[:128] == ref_seeds and inst[:128] == ref_inst, 'shared seed/instruction contract')
        count = 200 if n == 200 else 128
        require(len(seeds) == len(set(seeds)) == count, 'scaling sample count')
        require(sum(outcomes) == int(row['success']), 'scaling successes')
        require(sum(outcomes[:128]) == int(row['shared128_success']), 'shared-128 successes')
        seconds = sum(r['process_seconds'] for r in selected)
        close(seconds, row['seconds'], 'scaling process time')
        close(count * 3600 / seconds, row['throughput'], 'scaling throughput')
        close(seconds / count, row['seconds_per_episode'], 'scaling mean process cost')
        peak = max(v for r in selected for v in gpu_samples[r['run_id']])
        close(peak, row['gpu3_peak_mib'], 'sampled GPU peak')
        close(peak / total_mib * 100, row['gpu3_peak_percent'], 'sampled GPU capacity ratio')
    require(len(groups) == 15, 'scaling group count')

    for row in read('two_task_original.json'):
        selected = [by_id[key] for key in row['migrated_run_ids']]
        require(len(selected) == 4 and all(r['n'] == 16 for r in selected), '64-episode data lineage')
        actual = [(r['seed'], r['instruction']) for r in row['episodes']]
        expected = [(seed, text) for r in selected for seed, text in zip(r['seeds'], r['instructions'])]
        require(actual == expected and len(actual) == 64, '64-episode paired inputs')
        require(sum(r['success'] for r in row['episodes']) == row['success'], '64-episode original successes')

    replay = {r['run_id']: r for r in read('hammer_replay.json')}
    require(replay['closed_n64']['success'] == replay['replay_n64']['success'] == 48, 'hammer replay count')
    require(replay['closed_n64_repeat']['success'] == 38, 'hammer repeat count')
    require(replay['closed_n64']['seeds'] == replay['replay_n64']['seeds'] and
            replay['closed_n64']['successes'] == replay['replay_n64']['successes'], 'hammer paired replay')
    manifest = read('source_manifest.json')['files']
    require(all(key.startswith('source://roboseed-sim/') and len(value['sha256']) == 64
                for key, value in manifest.items()), 'source provenance format')
    require('/data/USERS/' not in '\n'.join(p.read_text() for p in DATA.glob('*.json')), 'nonportable source path')
    report = ROOT / 'docs/report/roboseed-sim/RoboSeed-Sim_zh.pdf'
    require(report.is_file() and report.read_bytes().startswith(b'%PDF-1.4'), 'reader PDF missing or incompatible')
    print('RoboSeed-Sim: 100 full-task rows, 1,600 outcomes, 800 historical pairs, '
          '96 small paired episodes, 48 scaling runs, GPU samples and N=64 replay checked.')


if __name__ == '__main__':
    verify()
