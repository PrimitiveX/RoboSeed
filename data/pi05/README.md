# π0.5 evidence and selection audit

[Home](../../README.md) · [Model](../../docs/action_models/pi05/README.md) · [Complete technical report](../../docs/report/README.md)

This November 24 addition contains one locally post-trained 50-task RoboTwin checkpoint and one local evaluation of released pi05_libero weights. It supplements the October 28 data; the historical twelve scored checkpoints and seventeen published model packages remain unchanged. The local RoboTwin weight URL is null until a real weight release is available.

| File | Scope |
| --- | --- |
| [metadata.json](metadata.json) | Checkpoint identities, effective settings, observation scope, dates and explicit unavailable measurements |
| [robotwin_episodes.jsonl](robotwin_episodes.jsonl) | All 10,000 selected valid task/scene/episode records, with seeds, source, success and execution details |
| [robotwin_retry_audit.json](robotwin_retry_audit.json) | Original/selected retry counts and seed audit; merge protocol and source-selection boundaries |
| [robotwin_task_results.csv](robotwin_task_results.csv) | 100 task/scene rows, each 100 valid episodes; original-valid and retry-selected counts |
| [robotwin_loss.csv](robotwin_loss.csv) | 29,548 rounded native console loss observations, steps 0–295470 in increments of ten |
| [libero_episodes.jsonl](libero_episodes.jsonl) | All 2,000 released-weight LIBERO records, seed 7; no local LIBERO training |
| [libero_tasks.csv](libero_tasks.csv) | Forty task rows, 50 episodes each |
| [libero_suite_results.csv](libero_suite_results.csv) | Four suite aggregates and separately attributed OpenPI reported references |
| [report_text.md](report_text.md) | Approved narrative source for the generated model/run documentation |
| [provenance.json](provenance.json) | External original evidence identities and SHA-256 hashes, using portable source identifiers |
| [manifest.json](manifest.json) | Hashes of packaged evidence, configuration records, figures and public report artifacts |

## Episode selection and limits

RoboTwin preserves 6,480 valid original episodes and selects 3,520 valid retries to fill unresolved `(task_config, task_name, episode)` slots. Expert-filter or unstable rejections do not count as completed rollouts and can change a retry candidate's seed. Valid originals are never replaced based on success. These records support this denominator and seed-selection protocol, not a claim of paired seeds across models.

LIBERO covers four suites, each with ten tasks and fifty default initial states per task. All episode keys are unique and have `status=completed`; none contains an evaluation error. The released checkpoint uses its own normalization assets. Its 97.20% result does not come from the locally trained RoboTwin model.

The source OpenPI tree contained local modifications. Its recorded HEAD is not a complete immutable training-code release. This package supports offline verification, figure regeneration and report compilation. It does not include model weights, simulator assets, demonstration datasets or a standalone end-to-end training implementation. The measured results, missing resource fields and unpublished weights remain separate states.

## Reproduce the packaged analysis

From the repository root:

```bash
python3 scripts/generate_docs.py
python3 scripts/verify_pi05.py
python3 scripts/draw_pi05_figures.py
python3 scripts/sync_pi05_report.py --article-root ../report
python3 scripts/verify.py --write-manifest
python3 scripts/verify.py
```

Figure generation needs NumPy and Matplotlib; the full report needs XeLaTeX and the documented packages. These commands do not launch policies or simulators and do not require GPUs. See [report management instructions](../../docs/report/README.md) and [portable recorded settings](../../configs/README.md#π05-recorded-settings).

## Existing project ownership and layout

The authoritative LaTeX, tables and figure generation remain in the separate roboseed report project. This Git repository contains presentation pages, public evidence, configuration snapshots, figure companions and the compiled PDF. Local publication plans and large model weights remain outside Git in the report handoff and existing hf_ckp model pipeline. Run the sync command only after rebuilding and validating the article; then refresh public manifests.
