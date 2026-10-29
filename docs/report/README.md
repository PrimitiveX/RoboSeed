# RoboSeed technical report

[Home](../../README.md) · [Documentation](../README.md) · [Experimental findings](../findings/README.md)

**RoboSeed: Multidimensional Evaluation of Vision–Language–Action and World–Action Models** · October 2026 · October 28 evidence snapshot, report updated October 29.

[Read the technical report (PDF)](RoboSeed.pdf)

The 41-page report connects capability, downstream training and deployment affordability, research value and reproduction evidence. It covers six completed ABot-M0 RoboTwin backbones, independent Qwen3.5-4B policies on LIBERO, RoboCasa and CALVIN, and zero-shot LIBERO-plus evaluation. LingBot-VLA 2.0, OpenWAM and LiLa-WAM add official/local checkpoint comparisons; the PX harness supplies systems measurements.

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

The [figure directory](../figure/results/) contains 17 figure sets in SVG, PDF and PNG. Figures 1–2 describe the project and ABot; 3–6 cover backbone budgets, resources, convergence and task profiles; 7–10 cover robustness, RoboCasa and CALVIN; 11 shows evaluation profiles; 12–14 show the added method experiments; 15–17 show their architectures.

[Refresh provenance](../../data/report_refresh.json) records hashes of the report and imported source data. [Packaged hashes](../../data/release_manifest.json) identify the distributed files. The PDF retains its research snapshot; current ModelScope publication links are maintained separately in the [release registry](../releases/README.md).

The [reproduction guide](../reproduction/README.md) explains the packaged analysis and external training/evaluation dependencies. Results with different task interfaces, inherited priors or evaluators are not controlled architecture comparisons. Missing Randomized outcomes, serving memory/p95 measurements and independently verified LiLa H200 adaptation cost remain explicit.

## Citation and attribution

Use the [repository citation](../../README.md#citation) or [CITATION.cff](../../CITATION.cff). Also cite the original models and benchmarks linked from each experiment. The report's architecture descriptions and mechanisms remain attributed to their original authors.
