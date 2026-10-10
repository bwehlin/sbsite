"""Generate the highlight banner figures (SVG, transparent, for the espresso band).

Run with stablebear 0.5.1b1 and matplotlib installed:
    python assets/highlights/make_figures.py

Colours come from the dark theme in design/tokens.json, which reads on the
espresso band. Figures carry no text: the slide copy explains them.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import stablebear as sb
from stablebear import persistence

HERE = Path(__file__).parent
TOKENS = json.loads((HERE.parent.parent / "design" / "tokens.json").read_text())
C = {t["name"]: t["value"]["dark"] for t in TOKENS["color"]["tokens"]}
TOKENS_LIGHT = {t["name"]: t["value"]["light"] for t in TOKENS["color"]["tokens"]}
S1, S2, MUTED = C["espresso"], C["honey"], C["ink-muted"]
SIZE = (6.4, 4.0)  # 16:10, matches the slide figure box
plt.rcParams.update({"svg.hashsalt": "stablebear", "svg.fonttype": "none"})


def figure():
    fig, ax = plt.subplots(figsize=SIZE)
    fig.patch.set_alpha(0)
    style(ax)
    return fig, ax


def style(ax):
    ax.set_facecolor("none")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.set_xticks([])
    ax.set_yticks([])


def save(fig, name):
    fig.savefig(HERE / name, transparent=True, bbox_inches="tight", pad_inches=0.05,
                metadata={"Date": None})
    plt.close(fig)


def steps(ax, pcf, grid, **kw):
    ax.plot(grid, np.asarray(pcf(grid)).ravel(), drawstyle="steps-post", **kw)


# 1. Bootstrapping local topology: 100 Gaussian-weighted samples around a query point at a
# ring's right edge (settings from the relative subsampling tutorial). The tutorial's clumps,
# blob and ring are rearranged to wrap over the top and left, leaving the bottom right for the
# stable ranks.
np.random.seed(5)
clumps = np.vstack([
    0.13 * np.random.randn(10, 2) + [-0.8, -0.6],
    0.13 * np.random.randn(10, 2) + [-0.8, 0.6],
    0.13 * np.random.randn(10, 2) + [0.45, 0.0],
]) + [-2.9, -1.1]
blob = 0.55 * np.random.randn(120, 2) + [-1.1, 0.9]
ring = np.random.randn(120, 2)
ring = 1.1 * ring / np.linalg.norm(ring, axis=1, keepdims=True)
ring += 0.22 * np.random.randn(120, 2) + [2.2, 1.3]
reference = sb.PointCloud(np.vstack([clumps, blob, ring]))
points = np.asarray(reference)
query = np.array([3.2, 1.3])
distribution = sb.distributions.Gaussian(0, 0.5)

samples = sb.random.subsample_relative(
    reference, query=query[None], n_points=30, n_samples=100,
    replace=True, discard_duplicates=True,
    distribution=distribution, generator=sb.random.Generator(seed=5),
)
ranks = persistence.barcode_to_stable_rank(
    persistence.compute_persistent_homology(samples, max_dim=0, reduced=True))[0, :, 0]
# Colour every point by its sampling weight around the query.
weights = np.asarray(distribution.weight(np.linalg.norm(points - query, axis=1)))

# Point cloud over the whole figure, stable ranks in the bottom right corner.
fig, ax = figure()
ax.axis("off")
ax.set_position([0, 0, 1, 1])
# Unlikely points muted, likely ones solid gold; the query in latte.
cmap = LinearSegmentedColormap.from_list("weight", [MUTED, S2])
t = np.clip(weights / np.percentile(weights, 99), 0, 1)
colours = cmap(t)
colours[:, 3] = 0.6 + 0.4 * t
order = np.argsort(weights)
ax.scatter(*points[order].T, c=colours[order], s=30, linewidths=0)
ax.scatter(*query, color=S1, s=140, edgecolors=TOKENS_LIGHT["espresso"], linewidths=2)
ax.set_aspect("equal")
ax.set_xlim(-4, 4)
ax.set_ylim(-2.4, 2.9)

curves = fig.add_axes([0.52, 0.04, 0.46, 0.36])
style(curves)
grid = np.linspace(0, 0.6, 600, dtype=np.float32)
for s in range(20):
    steps(curves, ranks[s], grid, color=S2, alpha=0.3, linewidth=1)
steps(curves, sb.mean(ranks), grid, color=S1, linewidth=3)
curves.set_xlim(grid[0], grid[-1])
curves.set_ylim(bottom=0)
save(fig, "local-topology.svg")

# 2. Into existing algorithms: a PCF evaluated on a grid (as the tutorial does with stable
# ranks, with fewer grid points so each one shows) becomes a feature vector for a small neural
# network. The PCF is made up for the picture: Betti-curve-like steps that rise and fall.
curve = sb.Pcf(np.array([
    [0.00, 0], [0.05, 1], [0.12, 3], [0.20, 2], [0.27, 4], [0.36, 6], [0.42, 5],
    [0.50, 7], [0.60, 4], [0.67, 5], [0.75, 3], [0.83, 2], [0.90, 1], [1.00, 0],
], dtype=np.float32))
values = np.array([0, 1, 3, 2, 4, 6, 5, 7, 4, 5, 3, 2, 1, 0], dtype=np.float32)
end = 1.1
n_grid = 12
grid = np.linspace(0, end, n_grid + 2, dtype=np.float32)[1:-1]
features = np.asarray(curve(grid)).ravel()
shade = LinearSegmentedColormap.from_list("feature", [C["espresso-tint"], S2])(features / values.max())

fig, ax = figure()
ax.axis("off")
ax.set_aspect("equal")
ax.set_xlim(0, 8)
ax.set_ylim(0, 5)
# The curve, its axes and the grid points, scaled into x 0.1-3.1, y 0.6-4.4.
X = lambda t: 0.1 + 3.0 * t / end
Y = lambda v: 0.6 + 3.8 * v / values.max()
ax.plot([X(0), X(0)], [Y(0), Y(values.max())], color=MUTED, linewidth=1)
ax.plot([X(0), X(end)], [Y(0), Y(0)], color=MUTED, linewidth=1)
dense = np.linspace(0, end, 2000, dtype=np.float32)
ax.plot(X(dense), Y(np.asarray(curve(dense)).ravel()), drawstyle="steps-post", color=S1, linewidth=2.5)
for t, v, c in zip(grid, features, shade):
    ax.plot([X(t), X(t)], [Y(0), Y(v)], color=MUTED, linewidth=1, alpha=0.4)
    ax.scatter(X(t), Y(v), color=c, edgecolors=S2, s=40, linewidths=1.2, zorder=3)
# The feature vector: one cell per grid point, shaded by its value.
cell = 3.8 / n_grid
cells = [(4.0, 4.4 - (k + 1) * cell) for k in range(n_grid)]
# A small network: every cell feeds every hidden unit, the hidden units feed two outputs.
hidden = [(5.9, 2.5 + (k - 2.5) * 0.7) for k in range(6)]
outputs = [(7.4, 2.5 + (k - 0.5) * 0.9) for k in range(2)]
for x, y in cells:
    for hx, hy in hidden:
        ax.plot([x + 0.5 * cell, hx], [y + 0.5 * cell, hy], color=MUTED, linewidth=0.6, alpha=0.25)
for hx, hy in hidden:
    for ox, oy in outputs:
        ax.plot([hx, ox], [hy, oy], color=MUTED, linewidth=0.8, alpha=0.4)
for (x, y), c in zip(cells, shade):
    ax.add_patch(plt.Rectangle((x - 0.5 * cell, y), cell, cell, facecolor=c, edgecolor=S2,
                               linewidth=1, zorder=3))
ax.scatter(*zip(*hidden), color=S1, s=110, linewidths=0, zorder=3)
ax.scatter(*zip(*outputs), color=S2, s=140, linewidths=0, zorder=3)
save(fig, "features.svg")

# 3. Exact representations: the area between two PCFs is the L1 distance, a finite sum of rectangles
# over their breakpoints. The matrix holds it for every pair of 20 made-up nonincreasing PCFs
# (like stable ranks), the pictured pair among them.
rng = np.random.default_rng(3)
# Most PCFs are random staircases: a few big drops at random places (Dirichlet steps), ending
# at a random time and scaled to about the same area, so they differ in shape rather than size.
# The pictured pair is 7 height (1 - t / end)^power, set apart (low and early, high and late)
# so it never touches.
n = 20
pair = (4, 14)
counts = rng.integers(10, 16, n)  # breakpoints per PCF; the pictured pair has 10 and 15
counts[list(pair)] = 10, 15
ends = rng.uniform(0.6, 1.0, n)
shapes = {pair[0]: (0.75, 1.9, 0.85), pair[1]: (0.95, 0.8, 1.0)}  # height, power, end
pcfs = sb.zeros((n,))
for k in range(n):
    m = counts[k] - 1
    t = np.r_[0, np.arange(1, m) / m + rng.uniform(-0.3, 0.3, m - 1) / m, 1]
    if k in shapes:
        height, power, end = shapes[k]
        v = 7 * height * (1 - t[:-1]) ** power * rng.uniform(0.9, 1.1, m)
    else:
        end = ends[k]
        v = 1 - np.r_[0, np.cumsum(rng.dirichlet(np.full(m, 0.3)))[:-1]]
    t = t * end
    if k not in shapes:
        v *= 3 * rng.uniform(0.9, 1.1) / np.sum(v * np.diff(t))
    pcfs[k] = sb.Pcf(np.column_stack([t, np.r_[np.sort(v)[::-1], 0]]).astype(np.float32))
D = sb.pdist(pcfs)
matrix = np.array([[D[i, j] if i != j else 0 for j in range(n)] for i in range(n)])
f, g = pcfs[pair[0]], pcfs[pair[1]]
check = np.linspace(0, 0.999, 1000, dtype=np.float32)
assert (np.asarray(g(check)) > np.asarray(f(check))).all(), "the pictured curves must not touch"

fig, ax = figure()
ax.axis("off")
ax.set_aspect("equal")
ax.set_xlim(0, 8)
ax.set_ylim(0, 5)
# The two curves and the area between them, scaled into x 0.1-4.1, y 0.6-4.4.
top = max(np.asarray(f)[:, 1].max(), np.asarray(g)[:, 1].max())
X = lambda t: 0.1 + 4.0 * t
Y = lambda v: 0.6 + 3.8 * v / top
ax.plot([X(0), X(0)], [Y(0), Y(top)], color=MUTED, linewidth=1)
ax.plot([X(0), X(1)], [Y(0), Y(0)], color=MUTED, linewidth=1)
# The integral breaks into rectangles between consecutive breakpoints of either PCF: outline
# them all and shade the first few from the left, as if the sum were partway through.
rects = [r for r in sb.iterate_rectangles(f, g, b=1) if r.f_value != r.g_value]
for k, r in enumerate(rects):
    lo, hi = sorted((r.f_value, r.g_value))
    box = (X(r.left), Y(lo)), X(r.right) - X(r.left), Y(hi) - Y(lo)
    if k < 12:  # shaded, outlined in a light palette colour so the dashes show
        ax.add_patch(plt.Rectangle(*box, facecolor=S2, alpha=0.45, linewidth=0))
        ax.add_patch(plt.Rectangle(*box, facecolor="none", edgecolor=TOKENS_LIGHT["fur"],
                                   linewidth=0.8, linestyle=(0, (2, 2))))
    else:
        ax.add_patch(plt.Rectangle(*box, facecolor="none", alpha=0.6, edgecolor=MUTED,
                                   linewidth=0.8, linestyle=(0, (2, 2))))
# Each step holds on [t_i, t_{i+1}): a filled dot where it starts, an open one where it ends.
# Both end at height 0, drawn up to t = 1.
for pcf, colour in ((f, S1), (g, S2)):
    t, v = np.asarray(pcf).T
    ax.scatter(X(t[1:]), Y(v[:-1]), facecolor=C["espresso-tint"], edgecolor=colour, s=28,
               linewidths=1.5, zorder=6)
    ax.scatter(X(t), Y(v), color=colour, s=28, linewidths=0, zorder=6)
    if t[-1] < 1:  # carry the final zero step on to t = 1
        t, v = np.r_[t, 1], np.r_[v, 0]
    for a, b, h in zip(t[:-1], t[1:], v[:-1]):
        ax.plot([X(a), X(b)], [Y(h), Y(h)], color=colour, linewidth=2.5, zorder=5)
# The distance matrix, shaded by distance, in x 4.9-7.9, y 1.0-4.0 (centred on the curves).
cell = 3.0 / n
shade = LinearSegmentedColormap.from_list("distance", [C["espresso-tint"], S2])
lo, hi = np.percentile(matrix[~np.eye(n, dtype=bool)], [2, 98])
for i in range(n):
    for j in range(n):
        x, y = 4.9 + j * cell, 4.0 - (i + 1) * cell
        ax.add_patch(plt.Rectangle((x, y), cell, cell, facecolor=shade(np.clip((matrix[i, j] - lo) / (hi - lo), 0, 1)),
                                   edgecolor=MUTED, linewidth=0.3, zorder=3))
save(fig, "distances.svg")
