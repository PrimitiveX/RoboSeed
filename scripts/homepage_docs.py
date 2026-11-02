"""Build the homepage inventory and dated updates from packaged evidence."""
import csv
import json
from datetime import datetime


def homepage_tables(root, table, slug):
    def read(name):
        with (root / 'data' / name).open(newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    rows = []
    labels = {}

    def add(unit, label, path, benchmark, origin, result, count, cost):
        target = f'[{label}]({path})'
        labels[unit] = (target, benchmark)
        rows.append([target, benchmark, origin, result, count, cost])

    for r in read('robotwin_summary.csv'):
        add('abot_robotwin_' + r['backbone'], 'ABot-M0 · ' + r['backbone'],
            f"docs/experiments/abot-m0/robotwin/{slug(r['backbone'])}.md",
            'RoboTwin', 'Local',
            f"Clean {float(r['clean_pct']):.2f}%; Randomized {float(r['randomized_pct']):.2f}%; mean **{float(r['avg_pct']):.2f}%**",
            '5,000 episodes / scene', f"{float(r['gpu_hours']):.1f}")

    for name, key, filename in [('LIBERO', 'libero', 'libero_tasks.csv'),
                                ('LIBERO-plus', 'liberoplus', 'liberoplus_tasks.csv'),
                                ('RoboCasa GR1 Tabletop', 'robocasa', 'robocasa_tasks.csv')]:
        records = read(filename)
        success = sum(int(r['success']) for r in records)
        episodes = sum(int(r['episodes']) for r in records)
        pathkey = 'robocasa-tabletop' if key == 'robocasa' else key
        add('abot_' + key, 'ABot-M0 · Qwen3.5-4B',
            f'docs/experiments/abot-m0/{pathkey}/qwen3-5-4b.md', name,
            'Local · LIBERO weights reused' if key == 'liberoplus' else 'Local',
            f'**{100 * success / episodes:.2f}%**', f'{success:,}/{episodes:,}',
            'No extra training' if key == 'liberoplus' else 'See run record')
    cs = read('calvin_summary.csv')[0]
    add('abot_calvin', 'ABot-M0 · Qwen3.5-4B',
        'docs/experiments/abot-m0/calvin/qwen3-5-4b.md', 'CALVIN · ABCD → D', 'Local',
        f"Mean chain **{cs['avg_seq_len']} / 5**; five tasks {100 * int(cs['fully_completed']) / int(cs['sequences']):.1f}%",
        f"{int(cs['sequences']):,} sequences", f"{float(cs['gpu_hours']):.1f}")

    tasks = read('extension_tasks.csv')
    for unit in json.loads((root / 'data/extension_units.json').read_text()):
        if unit['method'] == 'ABot-M0':
            continue
        scores = []
        counts = []
        for scene in ['Clean', 'Randomized']:
            group = [r for r in tasks if r['unit'] == unit['id'] and r['scene'] == scene]
            success = sum(int(r['success']) for r in group)
            episodes = sum(int(r['episodes']) for r in group)
            scores.append(f'{scene} {100 * success / episodes:.2f}%' if episodes else f'{scene} —')
            if episodes:
                counts.append(episodes)
        key = {'LingBot-VLA 2.0': 'lingbot-vla2', 'OpenWAM': 'openwam', 'LiLa-WAM': 'lila-wam'}[unit['method']]
        label = unit['label'].replace('LingBot 6B', 'LingBot-VLA 2.0 · 6B')
        add(unit['id'], label, f'docs/experiments/{key}/robotwin/README.md',
            'RoboTwin', 'Released weights' if unit['origin'] == 'official' else 'Local budget run',
            '; '.join(scores), f'{counts[0]:,} episodes / evaluated scene',
            '—' if unit['gpu_hours'] is None else f"{unit['gpu_hours']:.3f}")

    # The 8B backbone exists only in the earlier, smaller diagnostic protocol.
    # Keep it visible without promoting it into the current comparison or timeline.
    historical = (root / 'docs/experiments/abot-m0/robotwin/pre-train-to-post-train-diagnostic.md').read_text()
    diagnostic = next(line.split('|')[2].strip() for line in historical.splitlines()
                      if line.startswith('| Local Qwen3-VL 8B '))
    rows.append(['[ABot-M0 · Qwen3-VL-8B](docs/experiments/abot-m0/robotwin/pre-train-to-post-train-diagnostic.md)',
                 'RoboTwin · historical diagnostic', 'Local pre-train → post-train',
                 'Clean ' + diagnostic, '500 episodes; 10 / task', 'Not established'])
    overview = table(['Model / experiment', 'Benchmark', 'Checkpoint origin', 'Key metrics',
                      'Evaluation counts', 'Local training GPU-hours'], rows)
    dates = json.loads((root / 'data/model_updates.json').read_text())['updates']
    if {r['id'] for r in dates} != set(labels) or len(dates) != len(labels):
        raise ValueError('Model updates must cover every homepage experiment exactly once')
    updates = []
    for record in sorted(dates, key=lambda r: r['result_updated_at'], reverse=True):
        stamp = datetime.fromisoformat(record['result_updated_at'])
        if stamp.utcoffset().total_seconds() != 0:
            raise ValueError('Model update times must use UTC')
        target, benchmark = labels[record['id']]
        updates.append([stamp.strftime('%Y-%m-%d %H:%M:%S'), target, benchmark])
    return overview, table(['Result artifacts last updated (UTC)', 'Model / experiment', 'Benchmark'], updates)
