# AMseed

We aim to give the robotics community **an honest and complete record of what it takes to train and evaluate action models**. Each release connects the model inputs and training settings to resource use, checkpoints, rollout protocol, and task-level outcomes. We train established action models with VLM backbones at different scales, and rapidly evaluate and share emerging techniques of interest to the community. The model, dataset, and VLM indexes below will grow with the project.

## Action models

| Action model | Current coverage | Details |
| --- | --- | --- |
| ABot-M0 | S1 → S2 diagnostics and direct S2 training | [Action model and run index](docs/action_models/abot_m0/README.md) |

## Datasets

| Dataset | Current status | Details |
| --- | --- | --- |
| RoboTwin | Four completed direct-S2 model evaluations; earlier S1 → S2 diagnostics | [Dataset and results](docs/datasets/robotwin/README.md) |
| LIBERO | One recorded 4-suite rollout result | [Dataset and results](docs/datasets/libero/README.md) |
| RoboCasa Tabletop | No training or rollout record supplied | [Dataset description and reporting template](docs/datasets/robocasa_tabletop/README.md) |
| CALVIN | No training or rollout record supplied | [Dataset description and reporting template](docs/datasets/calvin/README.md) |

## Base VLMs

| VLM | Size | Official upstream model | Experiments |
| --- | --- | --- | --- |
| Qwen3-VL | 2B | [Qwen3-VL-2B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct) | [Qwen3-VL index](docs/models/qwen3/README.md) |
| Qwen3-VL | 4B | [Qwen3-VL-4B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct) | [Qwen3-VL index](docs/models/qwen3/README.md) |
| Qwen3.5 | 0.8B | [Qwen3.5-0.8B](https://huggingface.co/Qwen/Qwen3.5-0.8B) | [Qwen3.5 index](docs/models/qwen3_5/README.md) |
| Qwen3.5 | 4B | [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) | [Qwen3.5 index](docs/models/qwen3_5/README.md) |
| Qwen3.5 | 9B | [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) | [Qwen3.5 index](docs/models/qwen3_5/README.md) |

**Upstream links describe the original VLM families.** The action-adapted training inputs named in our reports, and the outputs of our runs, need separate Hugging Face links and revision IDs; their placeholders are in the run pages.

## Reported results

| Action model · VLM | Dataset | Rollout successes | Experiment record |
| --- | --- | --- | --- |
| ABot-M0 · Qwen3-VL 2B | RoboTwin | Clean 4183/5000 (83.66%); Randomized 4195/5000 (83.90%) | [Run](docs/experiments/qwen3-2b-robotwin/README.md) |
| ABot-M0 · Qwen3-VL 4B | RoboTwin | Clean 4285/5000 (85.70%); Randomized 4267/5000 (85.34%) | [Run](docs/experiments/qwen3-4b-robotwin/README.md) |
| ABot-M0 · Qwen3.5 0.8B | RoboTwin | Clean 4038/5000 (80.76%); Randomized 4025/5000 (80.50%) | [Run](docs/experiments/qwen3_5-0_8b-robotwin/README.md) |
| ABot-M0 · Qwen3.5 4B | RoboTwin | Clean 4294/5000 (85.88%); Randomized 4256/5000 (85.12%) | [Run](docs/experiments/qwen3_5-4b-robotwin/README.md) |
| ABot-M0 · Qwen3.5 4B | LIBERO | 1,935/2,000 (96.75%), four suites | [Run](docs/experiments/qwen3_5-4b-libero/README.md) |



RoboTwin direct-S2 results each cover 50 tasks × 100 trials per evaluation setting, seed 0. Training used both Clean and Randomized trajectories; do not compare these figures to a clean-only leaderboard protocol without accounting for that difference. The LIBERO rate comes from success/failure markers in rollout video filenames over 40 tasks × 50 trials. [RoboTwin task results](docs/datasets/robotwin/task_results.md) · [LIBERO task results](docs/datasets/libero/task_results.md). [Earlier S1 → S2 diagnostics](docs/experiments/robotwin-s1-diagnostics/README.md) used 10 Clean trials per task and are reported separately.

**Reported but without completed outcomes:** [Qwen3.5 9B / RoboTwin](docs/experiments/qwen3_5-9b-robotwin/README.md). Details for any future dataset/model pair should be added only after a corresponding experiment record is available. Checkpoint release URLs, full raw logs, and immutable dataset revisions are pending where marked in the subdocuments.

## Document structure

```text
README.md                    Overview and linked indexes
docs/action_models/          Action-model descriptions
docs/models/                 Base VLM descriptions
docs/datasets/               Dataset descriptions and per-task counts
docs/experiments/            Run-specific training and evaluation records
```

This package contains only the documentation derived from the supplied experiment reports and official model/benchmark descriptions. Add `README.md` and `docs/` to the root of your own repository; the source code and installation steps are not included here.
