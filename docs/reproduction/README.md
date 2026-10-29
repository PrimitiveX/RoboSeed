# Reproduction guide

[Home](../../README.md) · [Documentation](../README.md) · [Experiment records](../experiments/README.md) · [Checkpoint registry](../releases/README.md)

## Reproduce the packaged analysis

Python 3.10 or later can verify all counts and generated pages without third-party dependencies:

```bash
python3 scripts/verify.py
python3 scripts/generate_docs.py --check
```

Install the pinned plotting dependencies to regenerate the ten core figure sets:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 scripts/generate_docs.py
python3 scripts/draw_figures.py
python3 scripts/verify.py
```

Run commands from the repository root. Generated diagrams and charts are saved as editable SVG/PDF and PNG previews under `docs/figure/results/`. Tables are derived from the packaged CSVs; the root README's surrounding prose remains editable. No access to the original experiment filesystem is required. The seven extension figure sets (11–17) are packaged report exports; their values and native loss selections can be checked from the imported data, while this plotting script regenerates figures 1–10.

## Repeat training and robot evaluation

The recorded experiments use local adaptations of ABot-M0, LingBot-VLA 2.0, OpenWAM and LiLa-WAM. This repository distributes configurations and analysis tools; it does not distribute that training implementation or its simulator adapters. The official source establishes the model's method, while local interface changes remain part of the recorded reproduction setting.

| Component | Source / record |
| --- | --- |
| Action model | [ABot-M0 branch](https://github.com/amap-cvlab/ABot-Manipulation/tree/ABot-M0) and [model record](../action_models/abot_m0/README.md) |
| VLM backbones | [Official model cards and coverage](../models/README.md) |
| Simulation and datasets | [Benchmark index](../datasets/README.md) with official implementations |
| Actual recorded settings | [Nine configuration files](../../configs/README.md) |
| Initialization and trained policies | [Public release status](../releases/README.md) |
| Evaluation evidence | [Counts, source hashes, and audit decisions](../../data/README.md) |

Resolve the dataset and action-adapted initialization paths against your implementation before using a recorded configuration. Confirm that its action normalization, feature width, state handling, and channel selection match the run page. The official stock VLM weights alone do not identify the exact action-adapted local initialization.

RoboTwin uses the recorded `13c3c47` evaluator revision with local interface/frame-sampling changes. LIBERO and RoboCasa counts are reconstructed from video filename verdicts; exact immutable evaluator revisions are not established by those counts. CALVIN records the inspected client semantics, including eight executed actions and a 360-step per-subtask limit. These details are needed before treating a new run as a matched reproduction.

### Select the matching run

| Experiment | Policy and training setting | Evaluation to match |
| --- | --- | --- |
| [RoboTwin backbone comparison](../datasets/robotwin/README.md) | Independent policy per backbone; Clean + Randomized demonstrations; 150k direct post-train updates | 50 tasks × 100 episodes in each scene; launch seed 0; unseen instructions |
| [LIBERO](../experiments/abot-m0/libero/qwen3-5-4b.md) | Independent Qwen3.5-4B policy; selected 40k checkpoint | Four ten-task suites; 50 episodes per task |
| [LIBERO-plus](../experiments/abot-m0/liberoplus/qwen3-5-4b.md) | Same LIBERO checkpoint; no additional training | 10,030 unique perturbation variants; one episode each; recorded duplicate selection |
| [RoboCasa GR1 Tabletop](../experiments/abot-m0/robocasa-tabletop/qwen3-5-4b.md) | Independent Qwen3.5-4B policy; 50k updates; 29 absolute joint targets | 24 tasks × 50 episodes; 720-step limit; 12 executed actions per chunk |
| [CALVIN](../experiments/abot-m0/calvin/qwen3-5-4b.md) | Independent Qwen3.5-4B policy; ABCD data; 34k updates | D environment; stored 1,000 five-task sequences; 360 steps per subtask; eight executed actions |

Use the canonical run page and its linked YAML together. The recorded configuration describes the local implementation's schema; assigning environment variables alone does not expand `${...}` strings in YAML. Resolve dataset, action-adapted initialization, and output paths through your compatible loader or an edited copy before launching. Preserve the resolved copy with the new run.

Confirm the effective observation fields, action normalization, padding, channel order, active state conditioning, prediction horizon, and executed chunk length against the run record. For CALVIN, the inspected client supplies images and language, executes eight actions, and resets policy buffers between subtasks. Its configured 16-dimensional state layout and wrapper `replan_steps=5` do not establish the effective rollout behavior.

Published policy folders are linked in the checkpoint registry. Immutable initialization identities and compatible local implementation revisions remain reproduction dependencies. The commands above reproduce the available analysis; the repository does not currently supply a standalone training or rollout launcher.

### Compare the same metric

RoboTwin first aggregates 5,000 episodes in each scene, then equally averages the two scene rates. LIBERO and RoboCasa use equal episode counts per task. LIBERO-plus divides total selected successes by 10,030 variants; suite and category percentages have different denominators and should not be averaged equally.

For CALVIN, divide the sum of the five successful-prefix counts by 1,000 to obtain mean chain length. Fully completed chains are 571/1,000. Conditional task rates divide successes by reached attempts, which depend on earlier subtask outcomes. The input sequence list describes scheduled tasks and is not a per-sequence outcome trace. See [experimental findings](../findings/README.md) for the report's comparisons and interpretation.

## Preserve a new run

Save the resolved configuration and dependency versions, initialization revision, dataset revision, training log, checkpoint identity, and executed evaluator settings. Collect environment success counts and denominators before calculating aggregate rates. For continuous task chains, retain sequence-level outcomes and reached-attempt counts when available.

Use [CONTRIBUTING.md](../../CONTRIBUTING.md) to add the run and its evidence. Public URLs are added to the registry only after their artifacts exist; pending evaluations remain visibly separate.
