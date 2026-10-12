# RoboTwin · earlier pre-train → post-train diagnostics

[Home](../../../../README.md) · [RoboTwin](../../../datasets/robotwin/README.md)

The supplied `实验记录1.txt` documents local pre-train followed by post-train and comparisons involving upstream released weights. This is **not** the direct post-train experiment series: local pre-train/post-train runs used 100,000 steps per stage, and the recorded evaluation used 50 Clean tasks × 10 episodes (500 total) for each assessed checkpoint. The Qwen3-VL 4B local pre-train → post-train run had no supplied evaluation result.

| Recorded initialization / route | Clean successes / 500 | Recorded pre-train and post-train training time |
| --- | ---: | --- |
| Local Qwen3-VL 2B pre-train → local post-train, action horizon 16 in pre-train | 65/500 (13.0%) | 64.86 h + 53.12 h |
| Local Qwen3-VL 2B pre-train → local post-train, action horizon 50 in pre-train | 74/500 (14.8%) | 58.29 h + 42.85 h |
| Local Qwen3-VL 4B pre-train → local post-train | Not evaluated | 47.68 h + 56.92 h |
| Local Qwen3-VL 8B pre-train → local post-train | 73/500 (14.6%) | 80.35 h + 76.80 h |
| Upstream released RoboTwin model evaluated locally | 426/500 (85.2%) | Upstream training log not supplied |
| Upstream pre-train → locally trained post-train (`output_dim=1024`) | 375/500 (75.0%) | Upstream pre-train log absent; local post-train 31.21 h |
| Upstream pre-train → locally trained post-train (`output_dim=2560`) | 390/500 (78.0%) | Upstream pre-train log absent; local post-train 38.18 h |

The report names an official ABot-M0 pre-train checkpoint and [ABot-M0-RoboTwin2](https://huggingface.co/acvlab/ABot-M0-RoboTwin2) as upstream references, while explicitly saying that the exact upstream RoboTwin model initialization from the published pre-train checkpoint is unverified. Input and output HF links/revisions for **locally trained** checkpoints: not publicly released. Its 8B evaluation needed reruns after GPU scheduling errors; do not interpret the diagnostic percentages as leaderboard results or compare them directly with the 100-trial direct post-train series.

[All 50 task counts](pre-train-diagnostic-task-results.md). These historical results are kept outside the 100-episode backbone comparison.
