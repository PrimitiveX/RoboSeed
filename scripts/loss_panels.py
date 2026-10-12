"""Readable model-by-model training trajectories with defined tail summaries."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FixedLocator, NullLocator, LogFormatterMathtext


def training_loss_panels(loss_rows, evaluated_rows, training_only_rows):
    scores = {r['backbone']: float(r['avg_pct']) for r in evaluated_rows}
    # Ascending scale within each family makes comparisons easy to scan.
    names = [r['backbone'] for r in evaluated_rows + training_only_rows]
    if len(names) != 6 or len(set(names)) != 6:
        raise ValueError('Update the panel layout when the six-backbone coverage changes')
    names.sort(key=lambda n: (0 if n.startswith('Qwen3-VL-') else 1,
                              float(n.rsplit('-', 1)[1].removesuffix('B'))))
    fig, axes = plt.subplots(3, 2, figsize=(9.2, 8.0), sharex=True, sharey=True)
    fig.subplots_adjust(left=.095, right=.975, top=.89, bottom=.08,
                        hspace=.46, wspace=.22)
    fig.legend(handles=[Line2D([], [], color='#88b3d5', lw=1, alpha=.65,
                               label='Raw loss'),
                        Line2D([], [], color='#245f96', lw=2,
                               label='10-point moving average'),
                        Patch(facecolor='#edf4fa', edgecolor='#b8cddd',
                              label='Last 10k steps')],
               loc='upper left', bbox_to_anchor=(.085, .995),
               frameon=False, ncol=3, fontsize=11, handlelength=2,
               columnspacing=1.8)

    for idx, (ax, name) in enumerate(zip(axes.flat, names)):
        rows = sorted((r for r in loss_rows if r['backbone'] == name),
                      key=lambda r: int(r['step']))
        steps = np.array([int(r['step']) for r in rows])
        loss = np.array([float(r['action_dit_loss']) for r in rows])
        smoothed = np.convolve(loss, np.ones(10) / 10, mode='valid')
        tail = loss[(steps > 140000) & (steps <= 150000)]
        if len(tail) != 100 or np.any(loss <= 0) or loss.max() >= 2 or loss.min() <= 1e-4:
            raise ValueError(f'{name}: loss data outside the documented panel protocol')
        pending = name not in scores
        ax.axvspan(140, 150, color='#edf4fa', zorder=0)
        ax.axvline(140, color='#b8cddd', lw=.7, zorder=1)
        ax.plot(steps / 1000, loss, color='#88b3d5', alpha=.50, lw=.65, zorder=2)
        ax.plot(steps[9:] / 1000, smoothed, color='#245f96', lw=1.9, zorder=3)
        ax.set_title(f'({chr(97 + idx)}) {name}', loc='left',
                     fontsize=13, pad=10, color='#243447')
        ax.set(xlim=(0, 150), ylim=(1e-4, 2), yscale='log')
        ax.yaxis.set_major_locator(FixedLocator([1e-4, 1e-3, 1e-2, 1e-1, 1]))
        ax.yaxis.set_major_formatter(LogFormatterMathtext())
        ax.yaxis.set_minor_locator(NullLocator())
        ax.set_xticks([0, 50, 100, 150])
        ax.tick_params(labelsize=11, length=3, labelbottom=idx >= 4)
        ax.set_axisbelow(True)
        ax.grid(axis='y', color='#e1e8ef', linewidth=.6)
        if idx % 2 == 0:
            ax.set_ylabel('Action loss', fontsize=12)
        if idx >= 4:
            ax.set_xlabel('Training step (×1000)', fontsize=12)
        # Numeric annotations occupy the clear upper-right region of each panel.
        score = 'Evaluation pending' if pending else f'RoboTwin: {scores[name]:.2f}%'
        ax.text(.97, .96,
                f'Last 10k mean: {tail.mean() * 1000:.3f} × 10⁻³\n{score}',
                transform=ax.transAxes, fontsize=11, color='#243447',
                ha='right', va='top', linespacing=1.45,
                bbox=dict(facecolor='white', edgecolor='none', alpha=.95,
                          boxstyle='square,pad=.12'))
    return fig
