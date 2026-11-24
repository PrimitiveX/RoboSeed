"""Generate pi05 pages and index additions without changing the historical scoring cohort."""
import csv
import json


def build_pi05(root, table, link, fig, nav, notice):
    output = {}
    meta = json.loads((root / 'data/pi05/metadata.json').read_text())
    text = (root / 'data/pi05/report_text.md').read_text()
    robotwin, libero = text.split('## LIBERO Released-Weight Verification', 1)
    robotwin = robotwin.split('## π0.5\n', 1)[1].replace('### ', '## ')

    def document(path, body):
        for old, new in [('../../docs/figure/results/18_pi05_architecture.svg', '18_pi05_architecture'),
                         ('../../docs/figure/results/19_pi05_experiments.svg', '19_pi05_experiments')]:
            target = link('figure', f'docs/figure/results/{new}.svg', path).split('](', 1)[1][:-1]
            body = body.replace(old, target)
        output[path] = notice + body.rstrip() + '\n'

    for benchmark, body in [('robotwin', robotwin), ('libero', libero)]:
        path = f'docs/experiments/pi05/{benchmark}/README.md'
        name = 'RoboTwin' if benchmark == 'robotwin' else 'LIBERO released-weight verification'
        header = f'# π0.5 · {name}\n\n' + nav(path)
        header += '[Official implementation](https://github.com/Physical-Intelligence/openpi) · ' + link('Complete technical report', 'docs/report/README.md', path) + '\n\n'
        footer = '\n\n## Evidence and reproduction\n\n'
        footer += link('All task counts', f'docs/experiments/pi05/{benchmark}/task_results.md', path) + ' · ' + link('Packaged evidence and selection audit', 'data/pi05/README.md', path) + ' · ' + link('Run and checkpoint metadata', 'data/pi05/metadata.json', path) + '\n\n'
        footer += ('The local RoboTwin checkpoint has not been published; its public weight URL is null in the registry. The historical twelve-checkpoint score cohort is unchanged.\n' if benchmark == 'robotwin' else 'This is an evaluation of released weights, not local LIBERO post-train. The local RoboTwin weights are not reused here.\n')
        footer += '\n[1] Physical Intelligence, [OpenPI LIBERO example and reported results](https://github.com/Physical-Intelligence/openpi/tree/main/examples/libero).\n'
        document(path, header + body + footer)
    path = 'docs/action_models/pi05/README.md'
    document(path, '# π0.5\n\n' + nav(path) +
             'π0.5 uses a PaliGemma context backbone and a Gemma action expert with flow matching. RoboSeed adds a local 50-task RoboTwin post-train run and a separate verification of the released LIBERO checkpoint. Inherited base pre-train, local downstream adaptation and released-weight evaluation remain distinct.\n\n' +
             fig('18_pi05_architecture', 'π0.5 local RoboTwin reproduction interfaces.', path) + '\n' +
             table(['Experiment', 'Checkpoint origin', 'Completed result'], [
                 [link('RoboTwin', 'docs/experiments/pi05/robotwin/README.md', path), 'Local post-train from pi05_base', 'Clean 73.04%; Randomized 71.88%; mean 72.46%; 10,000 episodes'],
                 [link('LIBERO', 'docs/experiments/pi05/libero/README.md', path), 'Released pi05_libero evaluated locally', '1,944/2,000 (97.20%)']]) +
             '\nLocal LIBERO post-train and DROID experiments are not completed. The additional results are outside the historical twelve-checkpoint assessment profiles; no unmeasured resource scores or local weight-download URL is assigned.\n\n' + link('Evidence, configs and audit', 'data/pi05/README.md', path))

    with (root / 'data/pi05/robotwin_task_results.csv').open() as f:
        rows = list(csv.DictReader(f))
    path = 'docs/experiments/pi05/robotwin/task_results.md'
    task_rows = []
    for task in sorted({r['task'] for r in rows}):
        group = {r['scene']: r for r in rows if r['task'] == task}
        task_rows.append([task, group['demo_clean']['successes'] + '/100', group['demo_randomized']['successes'] + '/100'])
    document(path, '# π0.5 · all RoboTwin task counts\n\n' + nav(path) + table(['Task', 'Clean', 'Randomized'], task_rows) + '\n' + link('Original/retry source counts', 'data/pi05/robotwin_task_results.csv', path))
    with (root / 'data/pi05/libero_tasks.csv').open() as f:
        rows = list(csv.DictReader(f))
    path = 'docs/experiments/pi05/libero/task_results.md'
    document(path, '# π0.5 · all LIBERO task counts\n\n' + nav(path) + table(['Suite', 'ID', 'Instruction', 'Successes / 50'], [[r['suite'], r['task_id'], r['task'], r['successes']] for r in rows]) + '\n' + link('Released-checkpoint episode records', 'data/pi05/libero_episodes.jsonl', path))
    return output


def add_pi05_indexes(output, table, link):
    for page in ['docs/experiments/README.md', 'docs/action_models/README.md', 'docs/datasets/robotwin/README.md']:
        output[page] += '\n## π0.5 · November evidence addition\n\n' + table(['Experiment', 'Origin', 'Result'], [
            [link('π0.5 RoboTwin', 'docs/experiments/pi05/robotwin/README.md', page), 'Local post-train', '73.04% Clean; 71.88% Randomized; 10,000 episodes'],
            [link('π0.5 LIBERO', 'docs/experiments/pi05/libero/README.md', page), 'Released weights evaluated locally', '97.20%; 2,000 episodes']]) + '\n' + link('Model and reproduction boundary', 'docs/action_models/pi05/README.md', page) + ' · ' + link('Evidence and selection audit', 'data/pi05/README.md', page) + '\n\nThese observations supplement the October 28 study and are not assigned new five-dimension scores. Local weights are not yet published.\n'
