# RoboSeed-Sim evidence snapshot

[Report](../../docs/report/roboseed-sim/README.md) · [Experiment protocol](../../docs/experiments/roboseed-sim/README.md)

Evidence cutoff: **2026-11-20**. Initial packaging: **2026-11-22**. These dates describe the experiment snapshot and packaging separately; they do not imply experiments were rerun on the packaging date.

| File | Content |
| --- | --- |
| [protocol.json](protocol.json) | Model/checkpoint, system settings, sampling contract, timing boundaries and unavailable measurements |
| [full_task_results.csv](full_task_results.csv) | 100 scenario/task rows; integer outcomes, denominators and selected process duration |
| [full_episode_results.csv](full_episode_results.csv) | 1,600 selected clean/randomized task/seed outcomes and saved instructions |
| [historical_configurations.csv](historical_configurations.csv) | Seven manuscript configuration aggregates, imported from the preceding local audit |
| [historical_paired_results.csv](historical_paired_results.csv) | 800 clean task/seed outcomes for CPU N=1, GPU N=1 and GPU N=16 |
| [historical_task_profiles.json](historical_task_profiles.json) | Fifty task profiles corresponding to the paired results |
| [small_system_compare.json](small_system_compare.json) | Three tasks per scenario, original and migrated counts and times |
| [small_paired_episodes.csv](small_paired_episodes.csv) | 96 scenario/task/seed pairs with shared instructions and both outcomes |
| [two_task_original.json](two_task_original.json) | Original 64-episode outcomes and pointers to the four reused migrated batches |
| [scaling_runs.json](scaling_runs.json) | 48 runs with seeds, instructions, binary outcomes and process duration |
| [scaling_summary.csv](scaling_summary.csv) | Fifteen task/scale aggregates, common-128 success, throughput and sampled peak memory |
| [gpu_samples.csv](gpu_samples.csv) | 5,709 simulation-GPU samples, linked to scaling run IDs |
| [hammer_replay.json](hammer_replay.json) | Three selected N=64 diagnostic runs and their per-seed outcomes |
| [historical_repair_counts.json](historical_repair_counts.json) | Manuscript repair observations, explicitly transcribed rather than independent raw replay traces |
| [source_manifest.json](source_manifest.json) | Original input identities, byte counts and SHA-256 hashes |

Source IDs beginning `source://roboseed-sim/` identify original local evidence; they are not download URLs. Their hashes refer to original bytes. The root [release inventory](../release_manifest.json) hashes the files actually distributed in this repository. Machine-specific absolute source paths are retained only in a separate local map outside the public repository.

`process_seconds` and summary `seconds` are recorded evaluation-process durations, summed across selected completed runs. Seed screening and the complete interruption/retry history are excluded. Historical configuration aggregates and repair counts retain their earlier selection scopes; not all original raw traces are bundled. No simulator assets, model weights or training data are included in this snapshot.

The first 64 migrated episodes in the two-task comparison are reused from the N=16 scaling reference. N=16 through 128 share 128 seeds per task; N=200 shares their first 128 seeds and instructions and adds 72 episodes. Preserve this lineage when combining records.

```bash
python3 scripts/roboseed_sim/verify.py
```

Run the command from the repository root. It checks counts, paired inputs, workload lineage, throughput arithmetic, sampled GPU peaks and the selected hammer replay. Rechecking original-input hashes requires the external original files; the public check does not pretend those files were redistributed.
