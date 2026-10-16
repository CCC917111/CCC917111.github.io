"""Render the website figure from three published aggregate comparisons.

No original report, raw observations or individual predictions are used.
Source: DWTS Voting Analysis, commit 5efde6487cb36a92f0f8d9f3141ec6756e30af11,
results/exit_forecast_study/paired_differences.csv (v0.7.0).
Requires Matplotlib; the website itself has no Python/build dependency.
"""
from pathlib import Path
import csv
import math
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'figures'
PAPER, INK, BODY, BLUE, LINE = '#f2f0e9', '#181b1a', '#4d504e', '#2845cf', '#c9cbc3'
COMPARISONS = [
    ('choice_two', 'current_judges', 'Two-feature choice', 'current-score model'),
    ('selected_fixed_share', 'online_bayes', 'Selected fixed-share', 'fixed online mixture'),
    ('selected_tempered', 'online_bayes', 'Selected tempered', 'fixed online mixture'),
]


def read_rows():
    with (OUT / 'dwts-comparison.csv').open(newline='') as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != len(COMPARISONS):
        raise ValueError('Expected exactly three declared aggregate comparisons')
    for row, (candidate, baseline, _, _) in zip(rows, COMPARISONS):
        if (row['phase'], row['metric'], row['candidate'], row['baseline']) != (
                'nested_development', 'log_loss', candidate, baseline):
            raise ValueError('Unexpected comparison or population')
        if tuple(int(row[k]) for k in ('n_events', 'n_seasons', 'draws')) != (86, 12, 20000):
            raise ValueError('Comparisons must use the same declared evaluation population')
        for key in ('difference', 'lower', 'upper'):
            row[key] = float(row[key])
        lo, point, hi = (row[k] for k in ('lower', 'difference', 'upper'))
        if not all(math.isfinite(v) for v in (lo, point, hi)) or not lo <= point <= hi:
            raise ValueError('Invalid interval')
    return rows


def numeric_label(row):
    return f"{row['difference']:+.4f}  [{row['lower']:+.4f}, {row['upper']:+.4f}]"


def accessible_svg(path, rows):
    namespace = 'http://www.w3.org/2000/svg'
    ET.register_namespace('', namespace)
    tree = ET.parse(path)
    root = tree.getroot()
    root.set('role', 'img')
    root.set('aria-labelledby', 'chart-title chart-description')
    title = ET.Element(f'{{{namespace}}}title', {'id': 'chart-title'})
    title.text = 'Selected historical DWTS forecast comparisons'
    desc = ET.Element(f'{{{namespace}}}desc', {'id': 'chart-description'})
    desc.text = ('Paired differences in mean log loss on 86 outer-validation eliminations '
                 'across 12 seasons. Dots are candidate minus named baseline; lines are '
                 '95% whole-season bootstrap intervals from 20,000 draws. Negative '
                 'values favor the candidate. All three intervals cross zero. ' +
                 ' '.join(f'{label} versus {baseline}: {numeric_label(row)}.'
                          for row, (_, _, label, baseline) in zip(rows, COMPARISONS)) +
                 ' Exploratory historical evidence conditional on fitted predictions; '
                 'refitting, selection and repeated-exploration uncertainty are excluded. '
                 'This is not independent prospective validation.')
    root.insert(0, title)
    root.insert(1, desc)
    tree.write(path, encoding='utf-8', xml_declaration=True)


def render(rows, compact=False):
    plt.rcParams.update({
        'font.family': ['DejaVu Sans', 'sans-serif'], 'font.size': 11,
        'text.color': INK, 'axes.labelcolor': INK, 'xtick.color': BODY,
        'svg.fonttype': 'none', 'svg.hashsalt': 'dwts-portfolio-comparison-v1',
        'axes.unicode_minus': False,
    })
    fig = plt.figure(figsize=(3.6, 8.2) if compact else (8.4, 5.2), facecolor=PAPER)
    plot_box = [.10, .274, .85, .546] if compact else [.405, .32, .55, .47]
    ax = fig.add_axes(plot_box, facecolor=PAPER)
    ax.set(xlim=(-.11, .035), ylim=(-.45, 2.55), yticks=[])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.xaxis.set_major_locator(FixedLocator([-.10, -.05, 0, .03]))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: '0' if abs(x) < 1e-10 else f'{x:+.2f}'))
    ax.tick_params(axis='x', length=0, pad=9, labelsize=10.5 if compact else 10)
    ax.grid(axis='x', color=LINE, linewidth=.7, zorder=0)
    ax.axvline(0, color=INK, linewidth=1, linestyle=(0, (3, 3)), zorder=1)
    for index, (row, (_, _, label, baseline)) in enumerate(zip(rows, COMPARISONS)):
        y = 2 - index
        ax.errorbar(row['difference'], y,
                    xerr=[[row['difference'] - row['lower']], [row['upper'] - row['difference']]],
                    fmt='o', color=INK, ecolor=BLUE, elinewidth=1.8,
                    capsize=4, capthick=1.3, markersize=5, zorder=3)
        cy = plot_box[1] + plot_box[3] * ((y + .45) / 3)
        if compact:
            fig.text(.10, cy + .086, label, fontsize=11.5, weight='semibold', va='center')
            fig.text(.10, cy + .055, f'vs {baseline}', fontsize=10.5, color=BODY, va='center')
            fig.text(.10, cy - .042, numeric_label(row), fontsize=10.5, color=BODY, va='center')
        else:
            fig.text(.025, cy + .036, label, fontsize=11, weight='semibold', va='center')
            fig.text(.025, cy - .008, f'vs {baseline}', fontsize=10, color=BODY, va='center')
            fig.text(.025, cy - .052, numeric_label(row), fontsize=10, color=BODY, va='center')
    if compact:
        fig.text(.10, .965, 'Do the additions help?', fontsize=14, va='top', weight='semibold')
        fig.text(.10, .912, '86 historical outer-validation exits\n12 seasons · 95% paired intervals',
                 fontsize=10.5, color=BODY, va='top', linespacing=1.5)
        fig.text(.10, .19, 'Difference in mean log loss', fontsize=10.5)
        fig.text(.10, .151, 'Negative values favor the candidate.', fontsize=10, color=BODY)
        fig.text(.10, .105,
                 '20,000 whole-season bootstrap draws.\n'
                 'Fitted predictions held fixed; refitting,\n'
                 'selection and exploration uncertainty excluded.\n'
                 'Exploratory; no prospective validation.',
                 fontsize=9.5, color=BODY, va='top', linespacing=1.45)
    else:
        fig.text(.025, .94, 'Do the added features and adaptation help?', fontsize=17, va='top', weight='semibold')
        fig.text(.025, .85, '86 historical outer-validation exits · 12 seasons · 95% paired intervals',
                 fontsize=11, color=BODY, va='top')
        fig.text(.405, .22, 'Difference in mean log loss', fontsize=11)
        fig.text(.405, .169, 'Negative values favor the candidate.', fontsize=10, color=BODY)
        fig.text(.025, .095,
                 '20,000 whole-season bootstrap draws; fitted predictions held fixed.\n'
                 'Refitting, selection and exploration uncertainty excluded; no prospective validation.\n'
                 'Source: DWTS Voting Analysis v0.7.0 aggregate comparisons.',
                 fontsize=9, color=BODY, va='top', linespacing=1.45)
    name = 'dwts-comparison-mobile' if compact else 'dwts-comparison'
    svg_path = OUT / f'{name}.svg'
    fig.savefig(svg_path, facecolor=PAPER, metadata={'Date': None, 'Creator': 'Matplotlib'})
    accessible_svg(svg_path, rows)
    if not compact:
        fig.savefig(OUT / f'{name}.png', dpi=200, facecolor=PAPER,
                    metadata={'Software': 'Matplotlib', 'Title': 'Selected historical DWTS forecast comparisons'})
    plt.close(fig)


if __name__ == '__main__':
    selected = read_rows()
    render(selected)
    render(selected, compact=True)
    print('Rendered desktop SVG/PNG and compact SVG from three published aggregate comparisons.')
