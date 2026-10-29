"""Render report extensions and published checkpoint links from packaged evidence."""
import csv
import json


BUDGET_CONTEXT = (
    '**Experimental objective.** RoboSeed studies model behavior under practical, limited-hardware training budgets, '
    'using the ABot-M0 downstream study as the comparison reference. Some official training recipes require resources '
    'beyond this setting, so local runs adapt their batch sizes, training durations and execution settings to the available hardware. '
    'The goal is to compare models at comparable downstream training scales. The recorded runs below retain their actual budgets; '
    'batch size, updates, sample exposure and compute are not all equal across families. '
    'A local score below a released checkpoint therefore describes this budget-adapted recipe and does not establish that the original method is weaker.'
)


def budget_note(page, link):
    return BUDGET_CONTEXT + '\n\n' + link('Comparison scope and actual training budgets', 'docs/reproduction/comparison-protocol.md', page) + '\n\n'


FAMILIES = {
    'lingbot-vla2': {
        'name': 'LingBot-VLA 2.0', 'method': 'LingBot-VLA 2.0',
        'paper': 'https://arxiv.org/abs/2607.06403', 'figure': '12_lingbot_experiments',
        'architecture': '15_lingbot_architecture',
        'setup': 'Qwen3-VL-4B with 32 routed action experts (top-4 plus a shared expert) and depth/video teacher supervision. Local adaptation inherits the released foundation: Muon, three H200 GPUs, global batch 96, 50k updates, 55 state/action channels, three cameras, chunk length 50 and ten inference steps.',
        'protocol': 'Clean only, 50 tasks × 100 episodes, unseen instructions, seed 0, BF16 and compilation; four GPUs with three rollout slots each. Randomized evaluation is unavailable.',
        'interpretation': 'The released-weight reference and local budget run achieve 89.72% and 57.78% on the common local evaluator, a 31.94-point difference between training recipes. Local global batch 96 and 50k updates give 4.8M windows, versus 51.2M from the source recipe’s batch 1024 and 50k updates: 10.67× less exposure locally. This reduced-budget run implements the ABot-M0-referenced comparison objective; it does not repeat the full official adaptation recipe or measure the method’s attainable performance under that recipe. Exposure, teacher supervision, optimization and initialization effects are not isolated. The measured local interval is 174.365 H200 GPU-hours, excluding setup and final export.',
        'loss': ['ling_training_observations.csv'],
    },
    'openwam': {
        'name': 'OpenWAM', 'method': 'OpenWAM',
        'paper': 'https://arxiv.org/abs/2609.07398', 'figure': '13_openwam_experiments',
        'architecture': '16_openwam_architecture',
        'setup': 'Wan2.2-TI2V-5B and ActionDiT with joint self-attention; frozen Wan VAE and T5. Local adaptation inherits Foundation step 154000: four H200 NVL GPUs, BF16, ZeRO-2, AdamW, global batch 64 and 80k updates. Three views, 33-frame windows, stride four, 384 × 320 images; 20 physical end-effector channels in an 80-channel representation.',
        'protocol': 'Both scenes, each 50 tasks × 100 episodes; unseen instructions, seed 0, four GPUs and 16 rollout slots. Evaluator 0aeea2d requests observations at chunk start and checks success after every action. Both checkpoints share this adapted execution path.',
        'interpretation': 'The released-weight reference and local budget run have two-scene means of 93.84% and 91.35%, a 2.49-point difference between adaptation recipes. The local batch-64, 80k-update run processes 5.12M video windows, versus a source-reference estimate of 30.376M (118655 × 256). Local adaptation is scoped to the ABot-M0-referenced practical-budget study rather than the full official recipe. The local interval is 262.068 H200 GPU-hours; inherited foundation training is excluded. Local evaluation costs another 135.046 GPU-hours. Video windows and ABot examples are different training units; end-effector actions, inherited priors and evaluator differences also prevent attributing cross-family gaps to architecture alone.',
        'loss': ['openwam_training_observations.csv'],
    },
    'lila-wam': {
        'name': 'LiLa-WAM', 'method': 'LiLa-WAM',
        'paper': 'https://arxiv.org/abs/2608.03701', 'figure': '14_lila_experiments',
        'architecture': '17_lila_architecture',
        'setup': 'Frozen DINOv3 ViT-L/16 with compact future-feature prediction and action generation. Head camera at 320 × 240, 14 joint-action channels, 32 predicted actions, first 16 executed, ten flow steps and spline smoothing. The local evaluated artifact is stage-2 epoch four.',
        'protocol': 'Clean only, 50 tasks × five episodes on one H200 NVL with four workers. A task name selects precomputed visual transition tokens (task_cond.npy); the inspected policy ignores the instruction argument. These outcomes do not demonstrate unseen-language understanding.',
        'interpretation': 'The released-weight reference and local budget run achieve 224/250 (89.60%) and 222/250 (88.80%). The local artifact comes from completed saved prefixes through stage-1 epoch 12 and stage-2 epoch four; it does not establish completion of the configured 40-epoch stage-2 schedule. Its outcome belongs to this available-budget recipe. The difference is two successful episodes; five episodes per task do not establish equivalence. Randomized outcomes and independently verified H200 adaptation cost are unavailable, so an equal-compute comparison with ABot-M0 cannot be claimed. The approximately 1.273 GB package excludes the separately loaded DINOv3 encoder and may contain optimizer state, so it is not the complete deployment footprint.',
        'loss': ['lila_stage1_training_observations.csv', 'lila_stage2_training_observations.csv'],
    },
}


def build_extensions(root, table, link, fig, nav, notice):
    output = {}
    def put(page, text):
        output[page] = notice + text.rstrip() + '\n'
    def read(name):
        with (root / 'data' / name).open(newline='') as f:
            return list(csv.DictReader(f))
    units = json.loads((root / 'data/extension_units.json').read_text())
    tasks = read('extension_tasks.csv')
    packages = json.loads((root / 'data/modelscope_packages.json').read_text())['packages']
    def package_for(unit):
        prefix = {'ling_official': 'RoboSeed-LingBot-VLA2-6B-RoboTwin-official-',
                  'ling_local': 'RoboSeed-LingBot-VLA2-6B-RoboTwin-local-',
                  'openwam_official': 'RoboSeed-OpenWAM-Alpha-RoboTwin-official-',
                  'openwam_local': 'RoboSeed-OpenWAM-Alpha-RoboTwin-local-',
                  'lila_official': 'RoboSeed-LiLa-WAM-RoboTwin-official-stage2-',
                  'lila_local': 'RoboSeed-LiLa-WAM-RoboTwin-local-stage2-'}[unit['id']]
        return next(p for p in packages if p['package_id'].startswith(prefix))

    def comparison(page, selected=None):
        rows = []
        for unit in units:
            if unit['method'] == 'ABot-M0' or (selected and unit['method'] != selected):
                continue
            observed = [r for r in tasks if r['unit'] == unit['id']]
            values = []
            for scene in ['Clean', 'Randomized']:
                group = [r for r in observed if r['scene'] == scene]
                s = sum(int(r['success']) for r in group); n = sum(int(r['episodes']) for r in group)
                values.append(f'{s:,}/{n:,} ({100*s/n:.2f}%)' if n else '—')
            key = next(k for k, v in FAMILIES.items() if v['method'] == unit['method'])
            pkg = package_for(unit)
            label = unit['label'].replace(' official', ' · released weights').replace(' local', ' · local budget run')
            rows.append([link(label, f'docs/experiments/{key}/robotwin/README.md', page),
                         *values, '—' if unit['gpu_hours'] is None else f"{unit['gpu_hours']:.3f}",
                         f"[ModelScope]({pkg['public_url']})"])
        return table(['Checkpoint', 'Clean successes / episodes', 'Randomized successes / episodes',
                      'Local training GPU-hours', 'Weights'], rows)

    for key, info in FAMILIES.items():
        page = f'docs/experiments/{key}/robotwin/README.md'
        text = f"# {info['name']} · RoboTwin\n\n" + nav(page)
        text += f"[Original paper]({info['paper']}) · " + link('Technical report', 'docs/report/README.md', page) + '\n\n'
        text += budget_note(page, link)
        text += '## Setup and inherited components\n\n' + info['setup'] + '\n\n'
        text += fig(info['architecture'], info['name'] + ' architecture and reproduction interfaces.', page)
        text += '\n## Evaluation protocol\n\n' + info['protocol'] + '\n\n'
        text += comparison(page, info['method'])
        text += '\nReleased-weight rows are our local evaluations of official checkpoints, not scores copied from the original papers. Local-budget rows use our adapted training recipes.\n\n## Interpretation and measured cost\n\n' + info['interpretation'] + '\n\n'
        text += fig(info['figure'], info['name'] + ' checkpoint outcomes, native training losses, task profiles and recorded resources.', page)
        text += '\n## Evidence and downloads\n\n'
        text += ' · '.join(link(n, 'data/' + n, page) for n in info['loss']) + '\n\n'
        text += link('All task counts', f'docs/experiments/{key}/robotwin/task_results.md', page) + ' · ' + link('Checkpoint registry and package dependencies', 'docs/releases/README.md', page) + '\n\n'
        text += 'Each ModelScope folder contains its model card, available configuration and normalization assets. Follow that card for the compatible method implementation and external encoders. The branch `master` is mutable; the package registry records observed weight hashes.\n'
        put(page, text)
        model_page = f'docs/action_models/{key}/README.md'
        put(model_page, f"# {info['name']} reproduction\n\n" + nav(model_page) + budget_note(model_page, link) + info['setup'] + '\n\n' + info['protocol'] + '\n\n' + link('Results, resources, evidence and ModelScope weights', page, model_page) + f" · [Original paper]({info['paper']})\n")
        rows = [r for r in tasks if any(u['id'] == r['unit'] and u['method'] == info['method'] for u in units)]
        taskpage = f'docs/experiments/{key}/robotwin/task_results.md'
        put(taskpage, f"# {info['name']} · complete task outcomes\n\n" + nav(taskpage) + table(
            ['Checkpoint', 'Scene', 'Task', 'Successes / episodes', 'Success (%)'],
            [[r['unit'], r['scene'], r['task'], f"{r['success']}/{r['episodes']}", f"{100*int(r['success'])/int(r['episodes']):.2f}"] for r in rows]))

    page = 'docs/experiments/px-harness/README.md'
    rows = []
    for label, filename, elapsed in [('Original PX / W6', 'harness_original_all50_tasks.csv', 4185.99),
                                      ('Harness / W6', 'harness_w6_tasks.csv', 2222.52),
                                      ('Harness / W16', 'harness_w16_tasks.csv', 1814.54)]:
        group = read(filename); s = sum(int(r['success']) for r in group); n = sum(int(r['episodes']) for r in group)
        rows.append([label, f'{s}/{n}', f'{elapsed:.2f}', f'{2*elapsed/3600:.3f}', f'{n*60/elapsed:.2f}'])
    text = '# PX evaluation harness · systems reproduction\n\n' + nav(page)
    text += ('The full-task comparison uses ABot-M0 × Qwen3-VL-2B, two GPUs, all 50 Randomized tasks and ten episodes per task. '
             'The harness serves one model per GPU with simulation workers and shared episode queues. W denotes workers per GPU; batch cap is one.\n\n')
    text += table(['Entry', 'Successes / episodes', 'Startup-inclusive seconds', 'Allocated GPU-hours', 'Episodes/min'], rows)
    text += ('\nW6 increases observed episode throughput 1.88× over the original entry; W16 reaches 2.31×. '
             'Seed acceptance, instruction sampling and realized steps differ: W6/W16 use 32/24 replacement-seed episodes. '
             'These are systems observations, not matched capability gains or isolated neural-network latency measurements.\n\n'
             '## Matched-input topology and batch comparison\n\n')
    fresh = [r for r in read('harness_refresh.csv') if r['run'].startswith('px_4gpu_batch_compare_')]
    text += table(['Topology', 'Batch cap', 'Successes / episodes', 'Rollout seconds', 'Startup-inclusive seconds'],
                  [[r['topology'], r['batch_cap'], f"{r['successes']}/{r['episodes']}", r['wall_seconds'], r['end_to_end_seconds']] for r in fresh])
    text += ('\nThese three 12-task runs share task/seed/instruction inputs, but realized action counts differ. Increasing the batch cap from one to four did not improve this workload. '
             'Separate issue-bearing four-GPU runs and a failed ABot Qwen3.5-2B harness launch are excluded from capability conclusions; the latter does not invalidate the completed historical 100-episode-per-task 2B evaluation.\n\n')
    text += ' · '.join(link(n, 'data/'+n, page) for n in ['harness_refresh.csv', 'harness_original_all50_tasks.csv', 'harness_w6_tasks.csv', 'harness_w16_tasks.csv']) + '\n'
    put(page, text)

    page = 'docs/findings/assessment.md'
    assessment = json.loads((root / 'data/assessment.json').read_text())
    fmt = lambda v: '—' if v is None else f'{v:.2f}'
    text = '# RoboSeed evaluation framework · policy 1.1\n\n' + nav(page)
    text += budget_note(page, link)
    text += ('The decision unit is a checkpoint, training recipe, interface and evaluator tuple. The report defines five dimensions: '
             'capability P, downstream training affordability T, deployment affordability D, locally verified research value V and reproduction evidence R. '
             'These are declared decision rules, not a universal architecture ranking.\n\n'
             'P requires both Clean and Randomized outcomes. T uses the measured local H200 interval and fixed 64–1,024 GPU-hour anchors. '
             'D requires primary artifact size, warmed inference peak memory and p95 request latency; every D is missing in this snapshot. '
             'V and R follow the report’s binary evidence criteria. Missing components remain absent; no weights are renormalized and no composite is calculated without every required component.\n\n')
    text += table(['Checkpoint', 'P', 'T', 'D', 'V', 'R', 'Balanced composite'],
                  [[u['label'], *[fmt(u['scores'][k]) for k in ['P','T','D','V','R']], fmt(u['total']['balanced'])] for u in assessment['units']])
    text += '\n' + fig('11_assessment', 'Observed capability and downstream cost, with measurement coverage kept separate from a composite score.', page)
    text += '\nThe balanced profile uses weights 0.30 / 0.20 / 0.20 / 0.15 / 0.15. Training and deployment preference profiles, working Wilson intervals, evidence flags and anchors are retained in the ' + link('machine-readable assessment', 'data/assessment.json', page) + '. LiLa uses visual task tokens and five episodes per task; Clean-only results remain visible on the model page without inventing a two-scene P.\n'
    put(page, text)

    page = 'docs/reproduction/comparison-protocol.md'
    text = '# Comparison objective and training-budget scope\n\n' + nav(page) + BUDGET_CONTEXT + '\n\n'
    text += ('## What is being compared\n\n'
             'The scientific question is how different models perform at comparable downstream training scales on practical hardware, '
             'with ABot-M0 as the reference experiment. Official large-scale training requirements can exceed the resources available for this study; '
             'we therefore adapt local recipes and report their actual costs and outcomes. A lower local score is an observation about that configuration and budget, '
             'not a verdict on the original model or its full official training procedure.\n\n'
             'The present snapshot is an ABot-M0-referenced, budget-conscious comparison. Exact equalization remains a study objective: '
             'the existing runs have different update counts, batches, training units and inherited priors. '
             'They must not be described as an already completed equal-FLOP, equal-exposure or equal-GPU-hour experiment.\n\n'
             '## Actual downstream training scale\n\n')
    abot = [u for u in units if u['method'] == 'ABot-M0']
    ling = next(u for u in units if u['id'] == 'ling_local')
    wam = next(u for u in units if u['id'] == 'openwam_local')
    text += table(['Local model', 'Hardware / stopping point', 'Global batch', 'Recorded sample exposure', 'H200 training GPU-hours'], [
        ['ABot-M0 reference · six backbones', '4 H200 NVL; 150k updates', '64', '9.60M examples per backbone', f"{min(u['gpu_hours'] for u in abot):.3f}–{max(u['gpu_hours'] for u in abot):.3f}"],
        ['LingBot-VLA 2.0', '3 H200; 50k updates', '96', f"{ling['exposure']/1e6:.2f}M windows", f"{ling['gpu_hours']:.3f}"],
        ['OpenWAM', '4 H200 NVL; 80k updates', '64', f"{wam['exposure']/1e6:.2f}M video windows", f"{wam['gpu_hours']:.3f}"],
        ['LiLa-WAM', 'Saved stage-1 epoch 12 / stage-2 epoch 4', 'See package configuration', 'Not normalized to an ABot-equivalent count', 'Not independently verified'],
    ])
    text += ('\nThe measured few-GPU runs use H200-class accelerators; the recorded device types and GPU counts define the practical hardware scope of this snapshot. '
             'Sample exposure is batch × updates where available. An ABot example, a LingBot window and an OpenWAM video window contain different observations and have different compute costs. '
             'Reported H200 intervals cover downstream adaptation, excluding inherited foundation pre-train and unmetered setup, failed trials or engineering work.\n\n'
             '## How to read the reference rows\n\n'
             '**Released weights** means an official checkpoint evaluated through our local, family-specific execution path. '
             '**Local budget run** means our checkpoint trained with an adapted recipe. These references are evaluated locally; they are not original-paper leaderboard numbers. '
             'Within a family, official and local weights share the documented local evaluator. Across families, observations, action semantics, task conditioning and evaluation coverage still differ.\n\n'
             'LingBot uses 4.8M local windows against 51.2M in the source recipe; OpenWAM uses 5.12M against an estimated 30.376M. '
             'LiLa is evaluated at the saved stage-2 epoch-four checkpoint, with five episodes per task and visual task tokens. '
             'Keep these differences next to any score comparison and preserve the complete task counts.\n\n'
             '## Rules for future comparisons\n\n'
             'Declare the matched budget variable before training: for example, downstream allocated GPU-hours on the same accelerator, '
             'or sample exposure within a compatible training representation. Record the ABot-M0 reference, allowed hardware, batch, updates, precision, '
             'initialization and data coverage. Publish remaining mismatches, evaluator revisions and task denominators. '
             'Do not substitute the original paper’s larger-scale result for a locally evaluated reference, or attribute a budget-dependent difference to architecture alone.\n\n')
    text += link('Full experiment records', 'docs/experiments/README.md', page) + ' · ' + link('Original report snapshot', 'docs/report/README.md', page) + '\n'
    put(page, text)
    return output, comparison
