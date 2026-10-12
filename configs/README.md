# Recorded training configurations

[Home](../README.md) · [Reproduction guide](../docs/reproduction/README.md)

The nine YAML files in `abot-m0/` are copied from the saved configurations of the report's selected runs. Hyperparameters and architecture fields retain their recorded values. Machine-specific dataset and initialization paths are replaced with `${ROBOSEED_DATA_ROOT}` and `${ROBOSEED_VLM_BASE}`; output directories are mapped under `./outputs/`.

| Experiment | Configuration |
| --- | --- |
| RoboTwin · Qwen3.5-0.8B | [YAML](abot-m0/robotwin-qwen3-5-0-8b.yaml) |
| RoboTwin · Qwen3-VL-2B | [YAML](abot-m0/robotwin-qwen3-vl-2b.yaml) |
| RoboTwin · Qwen3-VL-4B | [YAML](abot-m0/robotwin-qwen3-vl-4b.yaml) |
| RoboTwin · Qwen3.5-4B | [YAML](abot-m0/robotwin-qwen3-5-4b.yaml) |
| RoboTwin · Qwen3.5-9B | [YAML](abot-m0/robotwin-qwen3-5-9b.yaml) |
| RoboTwin · Qwen3.5-2B, evaluation pending | [YAML](abot-m0/robotwin-qwen3-5-2b.yaml) |
| LIBERO · Qwen3.5-4B | [YAML](abot-m0/libero-qwen3-5-4b.yaml) |
| RoboCasa GR1 Tabletop · Qwen3.5-4B | [YAML](abot-m0/robocasa-tabletop-qwen3-5-4b.yaml) |
| CALVIN · Qwen3.5-4B | [YAML](abot-m0/calvin-qwen3-5-4b.yaml) |

These files record the local implementation's schema. They are not standalone launch scripts, and `${...}` values are placeholders that must be resolved by the user or a compatible loader. Training code, action-adapted initialization, and simulator adapters are external to this repository. Do not infer an effective state-input policy solely from a configured state dimension; the run pages distinguish configured layouts from inspected client behavior.
