# RoboSeed-Sim

[Project](../../../README.md) · [Report series](../README.md) · [Experiments](../../experiments/roboseed-sim/README.md)

**RoboSeed-Sim：面向视觉–语言–动作模型的 GPU 并行仿真评测系统**

*RoboSeed-Sim: GPU-Parallel Simulation and Evaluation for Vision–Language–Action Models*

RoboSeed 系列的独立系统报告，研究将 RoboTwin 的 LingBot-VLA 评测迁移至 GPU 并行管线后的任务表现、系统效率和环境规模扩展。中文初版整理于 **2026-11-22**，实验快照截至 **2026-11-20**。该版本是持续更新的研究报告；目前没有独立的 arXiv 编号。

[阅读中文 PDF](RoboSeed-Sim_zh.pdf) · [LaTeX 源稿](../../../reports/roboseed-sim/main.tex) · [编译说明](../../../reports/roboseed-sim/README.md) · [数据与证据](../../../data/roboseed_sim/README.md)

## 本版结果

| 实验 | 已记录结果 | 范围 |
| --- | --- | --- |
| 全任务迁移评测 | Clean 657/800（82.13%）；randomized 648/800（81.00%） | 各 50 任务、每任务 16 集 |
| 小规模系统对照 | Clean 吞吐为原始 TOPP/RT 的 1.91 倍；randomized 为 2.51 倍 | 三任务、每场景每套系统 48 集，相同 seed 和指令 |
| 两任务扩展对照 | 敲铃 4.93 倍、锤击 2.31 倍吞吐；成功率变化方向不同 | 每套系统每任务 64 集，迁移侧取规模实验前四批 |
| 单进程规模 | 三任务测试 N=16、32、64、128、200；N=200 显存采样峰值约为单卡容量的 98% | 仅 clean、单次实验；N=200 评测 200 集，其余各 128 集 |

吞吐按已记录的评测进程耗时合计计算，不含 seed 筛选及完整调度等待和全部中断重跑。上述倍数描述相应工作负载上的完整系统，不是单一组件的独立收益，也不是 50 任务整体加速比。

规模结果没有显示三个任务共同的成功率持续下降趋势；这不等于已经证明所有任务都不存在规模影响。N=128 到 200 的吞吐收益趋缓，但还不能确定普遍环境数上限或具体瓶颈。

## 阅读与复现

正文按全任务结果、修复验证、完整系统对照、固定动作诊断和环境规模扩展组织；附录给出截至 11 月 20 日的实现对照。真机部署保留结构，本版没有真机实验结论。

初版提供报告、处理后的结果快照、来源哈希、GPU 显存采样和可离线运行的绘图与核验脚本。仿真运行时、RoboTwin 任务适配和 VLA 服务实现仍是外部依赖，本次材料发布不等于已发布完整可运行的迁移管线。

```bash
python3 scripts/roboseed_sim/verify.py
python3 scripts/roboseed_sim/plot_figures.py
bash reports/roboseed-sim/build_report.sh
```

核验仅需 Python 标准库；绘图使用根目录的 Python 依赖。PDF 编译需要 XeLaTeX、Ghostscript 和源稿中指定的中文字体。见[源稿说明](../../../reports/roboseed-sim/README.md)。

## 系列关系与引用

[原 RoboSeed 报告](../RoboSeed.pdf)研究模型复现、能力与资源评估；本报告关注评测系统实现与效率。两者共享系列入口，分别保留实验协议和版本。原报告的 arXiv 编号对应原论文，不能作为本报告已经发表的编号。

引用当前快照时请注明 RoboSeed Team、完整标题及“中文初版，实验截至 2026-11-20”，并记录所使用的仓库提交。同时引用正文所列 ManiSkill3、RoboTwin 和 LingBot-VLA 的原始工作。
