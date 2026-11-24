# RoboSeed technical report

[Home](../../README.md) · [Documentation](../README.md) · [Experimental findings](../findings/README.md)

**RoboSeed: Multidimensional Evaluation of Vision–Language–Action and World–Action Models** · October 2026 · October 28 evidence snapshot, with a π0.5 evidence addition on November 24, 2026.

[Read the technical report (PDF)](RoboSeed.pdf) · [Public technical report on arXiv](https://arxiv.org/abs/2610.40026)

The complete report connects capability, downstream training and deployment affordability, research value and reproduction evidence. It covers six completed ABot-M0 RoboTwin backbones, independent Qwen3.5-4B policies on LIBERO, RoboCasa and CALVIN, and zero-shot LIBERO-plus evaluation. LingBot-VLA 2.0, OpenWAM and LiLa-WAM add official/local checkpoint comparisons; the PX harness supplies systems measurements.

The comparison is designed around practical, limited-hardware budgets, with ABot-M0 as the downstream reference. Local recipes adjust official batch sizes, training duration and execution settings where full official conditions exceed the available resources. Results describe these budget-adapted runs; released-weight reference rows are official checkpoints evaluated locally, not original-paper leaderboard scores. The [comparison protocol](../reproduction/comparison-protocol.md) lists actual training scales and distinguishes the goal of comparable budgets from exact equality of exposure or compute.

## Reading guide

| Topic | Repository companion |
| --- | --- |
| Project scope and reproduction principles | [Overview](../../README.md#overview) and [contribution guide](../../CONTRIBUTING.md) |
| ABot-M0 architecture, scaling and benchmark results | [Model record](../action_models/abot_m0/README.md) and [findings](../findings/README.md) |
| LingBot-VLA 2.0 predictive supervision and recipe gap | [Experiment and model weights](../experiments/lingbot-vla2/robotwin/README.md) |
| OpenWAM world/action coupling and adaptation budget | [Experiment and model weights](../experiments/openwam/robotwin/README.md) |
| LiLa-WAM compact latent prediction and visual task selection | [Experiment and model weights](../experiments/lila-wam/robotwin/README.md) |
| PX harness throughput, seeds and batch/topology measurements | [Systems record](../experiments/px-harness/README.md) |
| Five-dimension policy 1.1, missing data and sensitivity | [Assessment profiles](../findings/assessment.md) and [raw metadata](../../data/assessment.json) |
| Detailed task outcomes and source selection | [Experiment index](../experiments/README.md) and [data guide](../../data/README.md) |

## Figures and data

The [figure directory](../figure/results/) contains 19 figure sets in SVG, PDF and PNG. Figures 1–2 describe the project and ABot; 3–6 cover backbone budgets, resources, convergence and task profiles; 7–10 cover robustness, RoboCasa and CALVIN; 11 shows evaluation profiles; 12–14 show the added method experiments; 15–17 show their architectures.

[Refresh provenance](../../data/report_refresh.json) records hashes of the report and imported source data. [Packaged hashes](../../data/release_manifest.json) identify the distributed files. The PDF retains its research snapshot; current ModelScope publication links are maintained separately in the [release registry](../releases/README.md).

The [reproduction guide](../reproduction/README.md) explains the packaged analysis and external training/evaluation dependencies. Results with different task interfaces, inherited priors or evaluators are not controlled architecture comparisons. Missing Randomized outcomes, serving memory/p95 measurements and independently verified LiLa H200 adaptation cost remain explicit.

## Citation and attribution

Use the [repository citation](../../README.md#citation) or [CITATION.cff](../../CITATION.cff). Also cite the original models and benchmarks linked from each experiment. The report's architecture descriptions and mechanisms remain attributed to their original authors.

## November 24 π0.5 addition

The PDF above is the rebuilt full report, including [π0.5 local RoboTwin post-train](../experiments/pi05/robotwin/README.md), [released-weight LIBERO verification](../experiments/pi05/libero/README.md) and a complete task-count appendix. It preserves the original authors and historical assessment cohort. The arXiv link continues to identify the earlier public version.

The existing project separation is retained. LaTeX source, table rows, figures and source evidence are managed in the maintainer's separate `report/` project; this repository manages generated documentation, public evidence and the compiled PDF. No second independently maintained article project is added here.

Maintainers rebuild and validate the article with its existing `build.sh` and pi05 generation/validation scripts. From this repository, `python3 scripts/sync_pi05_report.py --article-root ../report` imports only verified public evidence, config snapshots, figure companions and the complete PDF. Then run `python3 scripts/generate_docs.py`, `python3 scripts/refresh_pi05_manifest.py`, and the standard repository verifier/manifest commands. The sync allowlist excludes private publication plans, model weights and credentials.

The added results are 7,246/10,000 (72.46%) on RoboTwin and 1,944/2,000 (97.20%) for released LIBERO weights. [Evidence and retry audits](../../data/pi05/README.md) preserve their different origins and selection protocols. Unavailable resource metrics remain explicit; no local weight URL has been published.
