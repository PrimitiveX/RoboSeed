"""Editable vector diagrams with explicit grouping, alignment, and feature flow."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon

INK = '#243447'
BLUE = '#245f96'
MID = '#6b98bf'
PALE = '#eef5fb'
BORDER = '#b8cddd'
GRAY = '#627487'
RULE = '#d8e2ea'


def canvas(width, height, figsize):
    fig, ax = plt.subplots(figsize=figsize)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set(xlim=(0, width), ylim=(0, height))
    ax.axis('off')
    return fig, ax


def text(ax, x, y, value, size=13, color=INK, weight='normal', **kwargs):
    return ax.text(x, y, value, fontsize=size, color=color, weight=weight,
                   ha=kwargs.pop('ha', 'left'), va=kwargs.pop('va', 'center'),
                   linespacing=1.4, **kwargs)


def frame(ax, x, y, w, h, fill='white', edge=BORDER, lw=1.1, radius=.10, dashed=False):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f'round,pad=0,rounding_size={radius}',
                       facecolor=fill, edgecolor=edge, linewidth=lw,
                       linestyle=(0, (4, 3)) if dashed else 'solid')
    ax.add_patch(p)
    return p


def node(ax, x, y, w, h, title, lines='', fill='white', edge=BORDER,
         dark=False, title_size=14, body_size=12.4):
    frame(ax, x, y, w, h, fill, edge)
    c = 'white' if dark else INK
    text(ax, x+w/2, y+h*.73, title, title_size, c, 'bold', ha='center')
    if lines:
        text(ax, x+w/2, y+h*.34, lines, body_size,
             '#e9f1f8' if dark else GRAY, ha='center')


def wire(ax, points, color=GRAY, dashed=False, arrow=True, lw=1.3):
    for a, b in zip(points[:-2], points[1:-1]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw,
                linestyle=(0, (4, 3)) if dashed else 'solid')
    if arrow:
        ax.annotate('', xy=points[-1], xytext=points[-2],
                    arrowprops=dict(arrowstyle='-|>', color=color, lw=lw,
                                    mutation_scale=12, shrinkA=0, shrinkB=3,
                                    linestyle=(0, (4, 3)) if dashed else 'solid'))
    else:
        a, b = points[-2:]
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw,
                linestyle=(0, (4, 3)) if dashed else 'solid')


def stage(ax, y, index, title, width=12.15):
    text(ax, .30, y, index, 11.3, BLUE, 'bold')
    text(ax, .80, y, title, 11.3, GRAY, 'bold')
    ax.plot([.80, width], [y-.15, y-.15], color=RULE, lw=.6)


def artifact_icon(ax, x, y, kind):
    if kind == 'weights':
        for k in range(3):
            frame(ax, x+k*.04, y-k*.07, .40, .26, fill=PALE, edge=MID, radius=.025)
            ax.plot([x+.09+k*.04, x+.29+k*.04], [y+.13-k*.07]*2, color=MID, lw=.8)
    elif kind == 'training':
        ax.plot([x, x, x+.5], [y+.4, y, y], color=MID, lw=.9)
        ax.plot([x+.04, x+.11, x+.2, x+.30, x+.43],
                [y+.34, y+.20, y+.12, y+.09, y+.07], color=BLUE, lw=1.5)
    else:
        for k in range(3):
            ax.add_patch(Rectangle((x, y+k*.13), .07, .07, facecolor=PALE, edgecolor=MID, lw=.7))
            ax.plot([x+.13, x+.46], [y+.035+k*.13]*2, color=MID, lw=.9)


def project_diagram():
    fig, ax = canvas(12.5, 5.89, (10.8, 4.92))
    ax.set_ylim(.20, 5.89)
    stage(ax, 5.69, '(a)', 'Experimental axes')
    xs = [.30, 4.38, 8.46]
    for x, title, lines in zip(xs,
                              ['VLA model', 'VLM configuration', 'Benchmark'],
                              ['ABot-M0\nFurther models (planned)',
                               'Backbone family + parameter scale\n0.8B / 2B / 4B / 9B',
                               'RoboTwin / LIBERO / RoboCasa\nCALVIN / LIBERO-plus']):
        node(ax, x, 4.16, 3.70, 1.27, title, lines, fill=PALE,
             title_size=15, body_size=12.2)
    for x in [4.12, 8.20]:
        text(ax, x, 4.81, '×', 19, MID, ha='center')
    stage(ax, 3.82, '(b)', 'Reproduction workflow')
    step_x = [.30, 3.43, 6.56, 9.69]
    for x, title, lines in zip(step_x,
                              ['Align interfaces', 'Train and monitor', 'Closed-loop rollout', 'Audit outcomes'],
                              ['Data + action semantics\nReference recipe',
                               'Costs + throughput\nLoss convergence',
                               'Fixed task protocol\nSuccess + failures',
                               'Check denominators\nTrace source records']):
        node(ax, x, 2.32, 2.49, 1.22, title, lines,
             title_size=13.0, body_size=11.7)
    for x in step_x[:-1]:
        wire(ax, [(x+2.49, 2.93), (x+3.13, 2.93)], color=BLUE, lw=1.4)
    stage(ax, 1.98, '(c)', 'Release artifacts')
    for x, title, lines, kind in zip(xs,
                                    ['Model package', 'Training record', 'Evaluation record'],
                                    ['Weights + matching configuration\nNormalization + versions',
                                     'Memory + GPU-hours + throughput\nRaw losses + convergence',
                                     'Task counts + rollout settings\nFailure analysis + audit'],
                                    ['weights', 'training', 'evaluation']):
        frame(ax, x, .36, 3.70, 1.30, fill='white', edge=MID)
        artifact_icon(ax, x+.21, 1.24 if kind == 'weights' else 1.09, kind)
        text(ax, x+.85, 1.35, title, 14, BLUE, 'bold')
        text(ax, x+1.85, .84, lines, 12.0, GRAY, ha='center')
    return fig


def rgb_views(ax, x, y):
    for k in [2, 1, 0]:
        px, py = x+k*.15, y+k*.11
        frame(ax, px, py, 1.05, .64, fill='white', edge=MID, radius=.035)
        ax.add_patch(Circle((px+.82, py+.47), .06, facecolor='#bad2e6', edgecolor='none'))
        ax.add_patch(Polygon([(px+.09, py+.12), (px+.35, py+.41),
                              (px+.56, py+.17), (px+.72, py+.30),
                              (px+.96, py+.12)], facecolor='#dae8f3', edgecolor='none'))
        for i in range(3):
            ax.add_patch(Rectangle((px+.13+i*.21, py+.12), .12, .08,
                                   facecolor=[MID, BLUE, '#b2cbdc'][i], edgecolor='none'))


def architecture_diagram():
    fig, ax = canvas(13.15, 5.12, (11.0, 4.12))
    ax.set_ylim(.20, 5.12)
    # Inputs have separate paths: language to VLM; images to both encoders.
    frame(ax, .30, 4.28, 2.25, .68, fill=PALE)
    text(ax, 1.425, 4.62, 'Language instruction', 12.2, INK, ha='center')
    frame(ax, .30, 2.54, 2.25, 1.39, fill=PALE)
    rgb_views(ax, .72, 2.99)
    text(ax, 1.425, 2.76, 'Multi-view RGB', 12.2, INK, ha='center')
    frame(ax, 3.09, 2.28, 2.86, 2.74, fill='#f7fafc', edge=RULE, radius=.13)
    node(ax, 3.32, 4.00, 2.40, .79, 'Replaceable VLM',
         'Qwen3-VL / Qwen3.5', title_size=13.2, body_size=11.6)
    node(ax, 3.32, 2.56, 2.40, .92, 'VGGT geometry',
         'Frozen spatial encoder', title_size=13.2, body_size=11.5)
    wire(ax, [(2.55, 4.62), (3.32, 4.62)], color=BLUE)
    wire(ax, [(2.55, 3.37), (2.85, 3.37), (2.85, 4.20), (3.32, 4.20)], color=BLUE)
    wire(ax, [(2.85, 3.37), (2.85, 3.02), (3.32, 3.02)], color=MID)
    ax.add_patch(Circle((2.85, 3.37), .026, facecolor=MID, edgecolor='none'))
    node(ax, 6.31, 3.62, 1.70, 1.17, 'Feature fusion',
         'Cross-attention', fill=BLUE, edge=BLUE, dark=True,
         title_size=12.0, body_size=11.7)
    node(ax, 6.31, 2.48, 1.70, .79, 'Projection',
         'Match VLM width', title_size=12.5, body_size=11.3)
    wire(ax, [(5.72, 4.39), (6.31, 4.39)], color=BLUE)
    wire(ax, [(5.72, 3.02), (6.01, 3.02), (6.01, 2.87), (6.31, 2.87)], color=MID)
    wire(ax, [(7.16, 3.27), (7.16, 3.62)], color=MID)
    # Action generation and execution, including optional state conditions.
    node(ax, 8.58, 3.62, 1.82, 1.17, 'Action expert',
         'AML / DiT-B\n4 integration steps', title_size=13.2, body_size=11.4)
    node(ax, 10.98, 3.62, 1.86, 1.17, 'Controller',
         'Unnormalize\nExecute chunk', title_size=13.2, body_size=11.6)
    wire(ax, [(8.01, 4.205), (8.58, 4.205)], color=BLUE, lw=1.4)
    wire(ax, [(10.40, 4.205), (10.98, 4.205)], color=BLUE, lw=1.4)
    node(ax, 8.42, 1.93, 2.15, 1.02, 'Conditioning',
         'Noise + time\nState, when provided', title_size=12.8, body_size=11.3)
    wire(ax, [(9.49, 2.95), (9.49, 3.62)], color=GRAY)
    node(ax, 10.98, .45, 1.86, 1.04, 'Environment',
         'Robot execution\nNew observation', title_size=12.8, body_size=11.2)
    wire(ax, [(11.91, 3.62), (11.91, 1.49)], color=BLUE, lw=1.4)
    text(ax, 12.12, 2.56, 'Execute', 10.7, GRAY, rotation=90)
    wire(ax, [(10.98, .97), (1.425, .97), (1.425, 2.54)], color=GRAY, dashed=True)
    text(ax, 5.0, 1.21, 'Closed-loop observation feedback', 11.2, GRAY, ha='center')
    return fig
