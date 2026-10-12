# RoboSeed technical report

[Home](../../README.md) · [Documentation](../README.md) · [Experimental findings](../findings/README.md)

**RoboSeed: Reproducing Vision–Language–Action Models** · RoboSeed Team · October 12, 2026

[Read the technical report (PDF)](RoboSeed.pdf)

The report presents the shared model-reproduction program and its first action-model study, ABot-M0. It connects backbone adaptation, training settings and costs, loss convergence, closed-loop performance, robustness, and observed failure patterns. Its current snapshot includes five completed RoboTwin backbone evaluations, a sixth training-only run, and Qwen3.5-4B records on LIBERO, LIBERO-plus, RoboCasa GR1 Tabletop, and CALVIN.

## Reading guide

| Report section | Topic | Repository companion |
| --- | --- | --- |
| 1 · Introduction | Computing budgets, project contributions, and coverage | [Project overview](../../README.md#overview) |
| 2 · Related Work | Open VLA models, action modeling, and robot evaluation | [Action-model index](../action_models/README.md) and [benchmarks](../datasets/README.md) |
| 3.1 · Reproducing Open VLA Models | Experimental axes, comparison principles, artifact protocol, and metrics | [Documentation guide](../README.md), [data schemas](../../data/README.md), and [contribution guide](../../CONTRIBUTING.md) |
| 3.2 · ABot-M0 | Architecture, backbone scale, resources, convergence, rollouts, and benchmark studies | [ABot-M0 record](../action_models/abot_m0/README.md) and [experimental findings](../findings/README.md) |
| Appendices | Detailed protocols, task outcomes, source audits, and CALVIN training evidence | [Experiment records](../experiments/README.md) and [packaged evidence](../../data/README.md) |

Additional action models will receive their own model sections and experiment records. Backbone substitutions remain grouped under the action model being reproduced.

## Figures and data

The [figure directory](../figure/results/) contains ten figure sets in editable SVG/PDF and PNG previews. Figures 1–2 explain the project and policy; Figures 3–6 cover RoboTwin scale, resources, loss, and tasks; Figures 7–10 cover robustness, RoboCasa, and CALVIN.

The repository's result tables and loss observations come from the audited report data. [Data documentation](../../data/README.md) describes the schemas, portable source identifiers, LIBERO-plus duplicate selections, and CALVIN duplicate-key audit. [Packaged hashes](../../data/release_manifest.json) identify the distributed data, recorded configurations, and this PDF.

To regenerate tables and figures, use the [reproduction guide](../reproduction/README.md). Analysis runs entirely from the packaged records. Training and rollouts require the external components described there.

## Citation and attribution

Use the [repository citation](../../README.md#citation) or [CITATION.cff](../../CITATION.cff) when referring to the experimental records and analysis. Also cite the original action model, VLM, and benchmark used in the experiment; their official references are linked from the model and benchmark pages. ABot-M0's action formulation and spatial-module design are attributed to its original authors.
