#!/usr/bin/env python3
"""Regenerate the four manuscript figure sets using only packaged evidence."""
from pathlib import Path
import csv
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data/roboseed_sim'
OUT = ROOT / 'reports/roboseed-sim/figures'
STYLES = [('click_bell', '#1f4f7c', 'o'), ('beat_block_hammer', '#288b96', 's'),
          ('pick_diverse_bottles', '#ad7650', '^')]


def read(name):
    return json.loads((DATA / name).read_text())


def save(fig, name):
    fig.savefig(OUT / (name + '.pdf'), bbox_inches='tight')
    fig.savefig(OUT / (name + '.png'), dpi=180, bbox_inches='tight')
    plt.close(fig)


def task_profiles():
    rows = sorted(read('historical_task_profiles.json'), key=lambda r: r['task'])
    fig, axes = plt.subplots(2, 1, figsize=(10.2, 7.5), layout='constrained')
    styles = [('cpu_n1', 'CPU N=1', '#9aa6b0', 's'),
              ('gpu_n1', 'GPU N=1', '#288b96', 'o'),
              ('gpu_n16', 'GPU N=16', '#1f4f7c', '^')]
    for j, ax in enumerate(axes):
        group = rows[j * 25:(j + 1) * 25]
        x = np.arange(len(group))
        for key, label, color, marker in styles:
            ax.plot(x, [r[key] * 100 / 16 for r in group], color=color, marker=marker,
                    markersize=3, linewidth=1.05, label=label, alpha=.9)
        ax.set_xticks(x, [r['task'] for r in group], rotation=67, ha='right', fontsize=6)
        ax.set_ylim(-3, 105)
        ax.set_yticks([0, 25, 50, 75, 100])
        ax.set_ylabel('Success rate (%)')
        ax.grid(axis='y', color='#dce3e8', linewidth=.6)
        ax.set_title(f"({'a' if j == 0 else 'b'}) Tasks {j * 25 + 1}–{(j + 1) * 25}",
                     loc='left', fontweight='bold')
        if j == 0:
            ax.legend(ncol=3, frameon=False, loc='lower left')
    save(fig, 'clean_task_profiles')


def small_compare():
    data = read('small_system_compare.json')
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.15), layout='constrained')
    x, width = np.arange(2), .32
    for i, (key, label, color) in enumerate([
            ('original', 'Original TOPP/RT', '#1f4f7c'),
            ('batch', 'Migrated N=16', '#288b96')]):
        success, throughput = [], []
        for scene in ('clean', 'randomized'):
            rows = [r[key] for r in data['results'][scene].values()]
            success.append(sum(r['success'] for r in rows) / 48 * 100)
            throughput.append(48 * 3600 / sum(r['wall_seconds'] for r in rows))
        for ax, values in zip(axes, (success, throughput)):
            bars = ax.bar(x + (i - .5) * width, values, width, color=color, label=label)
            ax.bar_label(bars, labels=[f'{v:.1f}' for v in values], padding=3, fontsize=8)
    for ax, title in zip(axes, ('(a) Success rate', '(b) Throughput')):
        ax.set_title(title, loc='left', fontweight='bold')
        ax.set_xticks(x, ['Clean', 'Randomized'])
        ax.grid(axis='y', color='#dce3e8', lw=.6)
        ax.set_axisbelow(True)
    axes[0].set_ylabel('Success rate (%)')
    axes[0].set_ylim(0, 110)
    axes[1].set_ylabel('Throughput (episodes/hour)')
    axes[1].set_ylim(0, 280)
    axes[0].legend(frameon=False, loc='lower left', fontsize=7)
    save(fig, 'small_system_compare')


def two_task_compare():
    runs = {r['run_id']: r for r in read('scaling_runs.json')}
    baseline = {r['task']: r for r in read('two_task_original.json')}
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.25), layout='constrained')
    for task, color, marker in STYLES[:2]:
        original = baseline[task]
        selected = [runs[key] for key in original['migrated_run_ids']]
        success = [original['success'] / 64 * 100,
                   sum(r['success'] for r in selected) / 64 * 100]
        throughput = [64 * 3600 / original['process_seconds'],
                      64 * 3600 / sum(r['process_seconds'] for r in selected)]
        for ax, values in zip(axes, (success, throughput)):
            ax.plot([0, 1], values, marker=marker, ms=5, lw=1.5, color=color, label=task)
            for i, value in enumerate(values):
                ax.annotate(f'{value:.1f}', (i, value), xytext=(0, 7),
                            textcoords='offset points', ha='center', fontsize=7, color=color)
    for ax, title, limit in [(axes[0], '(a) Success rate', 110),
                              (axes[1], '(b) Throughput', 560)]:
        ax.set_title(title, loc='left', fontweight='bold')
        ax.set_xticks([0, 1], ['Original TOPP/RT', 'Migrated N=16'])
        ax.set_xlim(-.23, 1.23)
        ax.set_ylim(0, limit)
        ax.grid(axis='y', color='#dce3e8', lw=.6)
    axes[0].set_ylabel('Success rate (%)')
    axes[1].set_ylabel('Throughput (episodes/hour)')
    axes[0].legend(frameon=False, loc='lower left', fontsize=7)
    save(fig, 'clean_two_task_systems')


def scaling():
    with (DATA / 'scaling_summary.csv').open() as f:
        rows = list(csv.DictReader(f))
    sizes = [16, 32, 64, 128, 200]
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.3), layout='constrained')
    axes = axes.ravel()
    for task, color, marker in STYLES:
        selected = sorted([r for r in rows if r['task'] == task], key=lambda r: int(r['n']))
        measures = [[int(r['shared128_success']) / 128 * 100 for r in selected],
                    [float(r['throughput']) for r in selected],
                    [float(r['gpu3_peak_percent']) for r in selected],
                    [float(r['seconds_per_episode']) for r in selected]]
        for ax, values in zip(axes, measures):
            ax.plot(sizes[:4], values[:4], marker=marker, ms=5, lw=1.5, color=color, label=task)
            ax.plot(sizes[3:], values[3:], marker=marker, ms=5, lw=1.5,
                    color=color, linestyle='--')
    titles = ['(a) Success on shared 128 seeds', '(b) Throughput',
              '(c) Simulation GPU memory', '(d) Process time per episode']
    for ax, title in zip(axes, titles):
        ax.set_title(title, loc='left', fontweight='bold')
        ax.set_xticks(sizes)
        ax.set_xlabel('Environments per process (N)')
        ax.grid(axis='y', color='#dce3e8', lw=.6)
    axes[0].set_ylabel('Success rate (%)')
    axes[0].set_ylim(0, 110)
    axes[1].set_ylabel('Throughput (episodes/hour)')
    axes[1].set_ylim(0, 700)
    axes[2].set_ylabel('Sampled peak memory (% of GPU 3)')
    axes[2].set_ylim(0, 110)
    axes[2].axhline(100, color='#929aa3', linewidth=.8, linestyle=':')
    axes[3].set_ylabel('Seconds / episode')
    axes[3].set_ylim(0, 15)
    axes[0].legend(frameon=False, loc='lower left', fontsize=7)
    save(fig, 'clean_scaling')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'pdf.fonttype': 42,
                         'axes.spines.top': False, 'axes.spines.right': False})
    for make in [task_profiles, small_compare, two_task_compare, scaling]:
        make()
    print('Regenerated four RoboSeed-Sim figure sets from packaged data.')


if __name__ == '__main__':
    main()
