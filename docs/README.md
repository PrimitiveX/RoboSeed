# RoboSeed documentation

[Home](../README.md) · [Technical report](report/README.md) · [Experiment index](experiments/README.md)

RoboSeed reproduces vision–language–action and world–action models. The October 28, 2026 evidence snapshot covers ABot-M0, LingBot-VLA 2.0, OpenWAM and LiLa-WAM, with a five-dimension evaluation framework and PX harness systems measurements. The project repository is **PrimitiveX/RoboSeed**; [17 model packages](releases/README.md) are published on ModelScope.

The comparison is designed around practical, limited-hardware budgets, with ABot-M0 as the downstream reference. Local recipes adjust official batch sizes, training duration and execution settings where full official conditions exceed the available resources. Results describe these budget-adapted runs; released-weight reference rows are official checkpoints evaluated locally, not original-paper leaderboard scores. The [comparison protocol](reproduction/comparison-protocol.md) lists actual training scales and distinguishes the goal of comparable budgets from exact equality of exposure or compute.

## Read the project

| Page | What it explains |
| --- | --- |
| [Evaluation framework](findings/assessment.md) | Five dimensions, explicit missing-data rules and recorded profiles |
| [PX evaluation harness](experiments/px-harness/README.md) | Full-task throughput and topology/batch measurements |
| [Experimental findings](findings/README.md) | Scale and budget comparisons, convergence versus execution, robustness, and failure patterns |
| [Technical report](report/README.md) | Full study, section guide, scientific figures, and citation |
| [Action models](action_models/README.md) | Reproduced methods, architecture, and adaptation choices |
| [VLM backbones](models/README.md) | Backbone families, nominal sizes, and experiment coverage |
| [Benchmarks](datasets/README.md) | Training setting, evaluation unit, and task-level outcomes |
| [All experiments](experiments/README.md) | Canonical run records and separate historical diagnostics |

## Follow an experiment

Start with an [action model](action_models/README.md), select its backbone and benchmark, and open the canonical run record. Each record describes training and execution settings, result denominators, resource measurements when available, and its configuration and evidence links.

For the RoboTwin comparison, begin with [ABot-M0 × Qwen3-VL-4B](experiments/abot-m0/robotwin/qwen3-vl-4b.md), then compare the [six evaluated backbones](datasets/robotwin/README.md). For robustness, follow the [LIBERO training record](experiments/abot-m0/libero/qwen3-5-4b.md) to [LIBERO-plus](experiments/abot-m0/liberoplus/qwen3-5-4b.md), which uses the same checkpoint. For continuous execution, read the [CALVIN ABCD → D record](experiments/abot-m0/calvin/qwen3-5-4b.md).

The [earlier pre-train → post-train studies](experiments/abot-m0/robotwin/pre-train-to-post-train-diagnostic.md) use a different training route and only ten episodes per Clean task. Their results remain in their own diagnostic section.

## Reproduce and contribute

| Task | Material |
| --- | --- |
| Check counts, generated pages, links, and packaged hashes | [Reproduction guide](reproduction/README.md) |
| Regenerate the figures and tables | [Analysis commands](reproduction/README.md#reproduce-the-packaged-analysis) |
| Inspect saved training settings | [Nine recorded configurations](../configs/README.md) |
| Understand schemas and source audits | [Results and evidence](../data/README.md) |
| Check whether a policy is publicly downloadable | [Checkpoint release registry](releases/README.md) |
| Add a model, run, or correction | [Contribution guide](../CONTRIBUTING.md) |

The release packages the report, results, audits, configurations, and analysis scripts. ModelScope policy folders are linked from the release registry; training implementations and simulator adapters remain external. Completed evaluation and downloadable weights are separate states.

## Interpret the results

RoboTwin reports equal weighting of Clean and Randomized scenes. LIBERO-plus weights variants by their actual counts. CALVIN reports the mean successful prefix of five-task sequences and conditional task rates over reached attempts. These metrics retain their own denominators.

RoboTwin training contains both Clean and Randomized demonstrations. CALVIN trains on ABCD and evaluates on D, which is included in training. Equal training updates do not mean equal compute, and measured workflow runtime does not identify single-request inference latency. The [findings page](findings/README.md) develops these distinctions alongside the observations they qualify.
