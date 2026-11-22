# RoboSeed-Sim manuscript

[Read the report](../../docs/report/roboseed-sim/README.md) · [Evidence](../../data/roboseed_sim/README.md)

The canonical source is [main.tex](main.tex). This initial Chinese manuscript uses evidence through November 20, 2026. Editable figures and their PNG previews are in [figures](figures/); the separate [plotting script](../../scripts/roboseed_sim/plot_figures.py) regenerates all four external manuscript figure sets from packaged data. The pipeline and aggregate-success diagrams are embedded as TikZ in the source.

From the repository root:

```bash
python3 scripts/roboseed_sim/plot_figures.py
bash reports/roboseed-sim/build_report.sh
```

Plotting uses the root Python requirements. Compilation needs XeLaTeX, Ghostscript, the TeX packages named in the source, and the fonts `AR PL UMing CN` and `Droid Sans Fallback`. On Debian/Ubuntu, the usual package set is `texlive-xetex texlive-latex-extra texlive-fonts-recommended texlive-lang-chinese fonts-arphic-uming fonts-droid-fallback ghostscript`.

The build writes temporary files to the ignored `_build/` directory and publishes the reader PDF to [docs/report/roboseed-sim/RoboSeed-Sim_zh.pdf](../../docs/report/roboseed-sim/RoboSeed-Sim_zh.pdf). Two XeLaTeX passes update references and the contents page. Ghostscript produces a PDF 1.4 reader copy with `-dAutoRotatePages=/None` so angled figure labels do not rotate a whole page.

Preserve the shared blue/teal/brown palette, fonts and line styles when changing figures. The dashed N=128-to-200 segments denote changed workload size; the success panel uses only common seeds, while throughput uses each run's complete workload.

The repository contains the complete manuscript inputs and processed evidence for offline analysis. Re-running simulation requires the external RoboTwin adapters, simulator assets, LingBot weights and policy service; these implementations are outside the scope of this initial report addition.
