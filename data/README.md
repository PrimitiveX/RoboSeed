# Results and evidence

[Home](../README.md) · [Experiment index](../docs/experiments/README.md)

This directory packages the records used in the October 12, 2026 RoboSeed report. Counts and loss observations are copied from its audited data. No model weights, demonstration videos, or simulation datasets are bundled.

## Result tables

| File | Unit and schema |
| --- | --- |
| [robotwin_summary.csv](robotwin_summary.csv) | Five complete backbones; success counts, percentage rates, training cost, memory readings, throughput, checkpoint size, and rollout time |
| [robotwin_training_only.csv](robotwin_training_only.csv) | Qwen3.5-2B training record; no completed evaluation score |
| [robotwin_tasks.csv](robotwin_tasks.csv) | 500 `(backbone, suite, task)` rows; `success`, `episodes`, `success_rate_pct` |
| [robotwin_loss.csv](robotwin_loss.csv) | Six training runs; `backbone`, `step`, `action_dit_loss` |
| [libero_tasks.csv](libero_tasks.csv) | 40 tasks; suite, task, successes, episodes, and percentage rate |
| [liberoplus_tasks.csv](liberoplus_tasks.csv) | 10,030 selected variants; suite, variant ID, category, binary success, episodes |
| [liberoplus_suite.csv](liberoplus_suite.csv) / [liberoplus_category.csv](liberoplus_category.csv) | Micro-averages with actual suite/category denominators |
| [robocasa_tasks.csv](robocasa_tasks.csv) | 24 GR1 Tabletop tasks; 50 episodes per task |
| [calvin_summary.csv](calvin_summary.csv) | Final training run, mean chain length, resource costs, and aggregate outcomes |
| [calvin_chain.csv](calvin_chain.csv) | Five successful-prefix counts, each over 1,000 sequences |
| [calvin_tasks.csv](calvin_tasks.csv) | 34 conditional task outcomes; denominators are reached attempts |
| [calvin_families.csv](calvin_families.csv) | Horizontal pushing, its left/right subsets, and remaining task types; subset rows overlap |
| [calvin_loss.csv](calvin_loss.csv) | 340 observations from the final 34k-update run |

Rates ending in `_pct` are percentages. The historical per-backbone RoboTwin CSVs under `docs/experiments/abot-m0/robotwin/` preserve their original three-column interface and use fractional rates in `[0, 1]`. The combined CSV contains the counts needed to check them.

## Source records and audits

- [source_manifest.json](source_manifest.json) records the report's collection time, original evidence sizes and SHA-256 hashes, and dataset-specific checkpoint mappings. Original filesystem paths are replaced with stable `source://` identifiers. These IDs are not download URLs. Weight sizes were checked locally; large weights were not hashed or copied.
- [video_index.csv](video_index.csv) preserves LIBERO, LIBERO-plus, and RoboCasa video filename verdicts, episode identifiers, and portable source IDs. The referenced videos remain outside this repository.
- [liberoplus_duplicates.json](liberoplus_duplicates.json) retains all alternatives for 101 repeated variant keys and the selected latest-mtime record. Three conflicting keys bound the aggregate result at 80.01%–80.04%.
- [calvin_results_source.json](calvin_results_source.json) preserves the original duplicate-key JSON bytes. Ordinary JSON loaders silently select the last `0` key; [calvin_audit.json](calvin_audit.json) explicitly retains both occurrences and explains why the final 1,000-sequence result was chosen over the ten-sequence smoke test.
- [calvin_eval_sequences.json](calvin_eval_sequences.json) is the input sequence list, rather than an independent outcome trace. [calvin_dataset_metadata.json](calvin_dataset_metadata.json) records the converted dataset's cameras, feature layout, counts, and frame rate.
- [checkpoints.json](checkpoints.json) lists nine verified local artifacts. `public_url` and `revision` remain `null` until an actual immutable public release is supplied. LIBERO-plus shares the LIBERO checkpoint.

The original result CSVs and CALVIN source JSON retain the report's values. Public JSON audits and the video index change only local path representations. The source manifest's hashes refer to the original evidence, while [release_manifest.json](release_manifest.json) hashes the files actually packaged here.

## Update and validate

Use complete counts with an explicit protocol when promoting a new result. Keep preliminary runs, duplicate alternatives, and training-only records separate from completed comparisons. Changes to dataset splits, observation/state handling, action channels, or executed chunk length belong in the run record.

```bash
python3 scripts/generate_docs.py
python3 scripts/verify.py
```

The generator updates result tables, task pages, and compatibility pages from these records. The verifier checks denominators, aggregates, duplicate selections, loss coverage, checkpoint mappings, generated content, relative links, and packaged file hashes.
