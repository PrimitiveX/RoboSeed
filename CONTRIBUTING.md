# Contributing to RoboSeed

[Home](README.md) · [Data schema](data/README.md) · [Reproduction guide](docs/reproduction/README.md)

## Add an action model

Create a dedicated section under `docs/action_models/<model>/README.md` and canonical run pages under `docs/experiments/<model>/<benchmark>/`. Describe the original architecture and cite its official implementation. Record reproduction choices separately from deliberate adaptations. Add the model to the action-model and experiment indexes; keep backbone variants within its own section.

ABot-M0 is the first section. Additional models should follow the same record structure without being described as ABot-M0 variants.

## Compare under practical training budgets

Use ABot-M0 as the downstream reference for the practical-budget study. State which hardware and budget variable are matched, and document changes from the source recipe when its full training requirements exceed available resources. Record actual batch, updates, sample exposure, inherited initialization and measured device time; call a comparison equal-scale only for variables that were actually matched. See the [comparison protocol](docs/reproduction/comparison-protocol.md).

Label official checkpoints evaluated locally as released-weight references, and locally adapted checkpoints as budget runs. Original-paper headline scores need separate attribution and protocol details. Explain any lower local outcome in the context of the observed training recipe and budget, without claiming that a resource difference alone caused it.

## Add or update an experiment

1. Record the dataset/split/revision, initialization identity, configured and executed action/state layouts, optimizer, learning rates, frozen modules, batch, updates, hardware, and training seed.
2. Supply complete task counts with denominators, evaluator revision, rollout seed, episode limits, language split, and execution chunk length. Preserve duplicate or preliminary records with an explicit selection rule.
3. Add loss observations, wall time, GPU count, measured resource values, and checkpoint size when available. Mark absent observations rather than assigning a guessed value.
4. Update the machine-readable results and checkpoint registry. Public URL/revision fields remain null until the actual artifacts are released. Promote a pending evaluation only when its complete protocol and counts are available.
5. Update the canonical documentation and generate tables and figures. For the current ABot-M0 pages and experimental findings, edit `scripts/generate_docs.py` or its input CSVs; root README tables are delimited by generated markers. Add future-model generation separately, retaining the shared indexes. Keep the documentation entry point and report guide aligned with the current release's scope.

## Check a change

```bash
python3 scripts/generate_docs.py
python3 scripts/generate_docs.py --check
python3 scripts/verify.py
```

If data, configs, or the report changed, refresh their packaged hash inventory after checking the source changes:

```bash
python3 scripts/verify.py --write-manifest
python3 scripts/verify.py
```

Regenerate affected figures with the plotting dependencies installed. Check their rendered labels and captions, especially legend placement and shared axes. Keep figure explanations in captions; avoid adding an overall title inside framework diagrams or the training-loss panel grid. Preserve existing compatibility paths when reorganizing pages.

Use **pre-train** and **post-train** in displayed documentation. Keep training-only records outside completed score comparisons. Use percent units for `_pct` fields, retain original fractional-rate compatibility CSVs, and distinguish episode success from CALVIN chain completion and conditional task rates.

Changes should describe the concrete experiment, evidence added, checks performed, and any unresolved release or protocol field. Cite the action model, VLM, and benchmark whose work the experiment builds on.
