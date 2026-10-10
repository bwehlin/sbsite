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

# 2-4. Disk vs annulus point clouds (from the PyTorch classifier tutorial).
rng = np.random.default_rng(42)


def disk(n):
    r, t = np.sqrt(rng.uniform(0, 1, n)), rng.uniform(0, 2 * np.pi, n)
    return np.column_stack([r * np.cos(t), r * np.sin(t)]).astype(np.float32)


def annulus(n):
    r, t = np.sqrt(rng.uniform(0.8**2, 1.2**2, n)), rng.uniform(0, 2 * np.pi, n)
    return np.column_stack([r * np.cos(t), r * np.sin(t)]).astype(np.float32)


half, n = 100, 60
clouds = sb.zeros((2 * half,), dtype=sb.pcloud32)
for i in range(2 * half):
    clouds[i] = disk(n) if i < half else annulus(n)
barcodes = persistence.compute_persistent_homology(clouds, max_dim=1)
h1_ranks = persistence.barcode_to_stable_rank(barcodes)[:, 1]
h1_betti = persistence.barcode_to_betti_curve(barcodes)[:, 1]

# 2. Stable ranks: every sample faint, the class means bold.
grid = np.linspace(0, 1.6, 800, dtype=np.float32)
fig, ax = figure()
for lo, colour in ((0, S1), (half, S2)):
    for i in range(lo, lo + 15):
        steps(ax, h1_ranks[i], grid, color=colour, alpha=0.3, linewidth=1)
    steps(ax, sb.mean(h1_ranks[lo:lo + half]), grid, color=colour, linewidth=3)
ax.set_xlim(grid[0], grid[-1])
ax.set_ylim(bottom=0)
save(fig, "stable-ranks.svg")

# 3. Betti curves: mean H1 Betti curve per class.
grid = np.linspace(0, 2.0, 800, dtype=np.float32)
fig, ax = figure()
for lo, colour in ((0, S1), (half, S2)):
    for i in range(lo, lo + 15):
        steps(ax, h1_betti[i], grid, color=colour, alpha=0.3, linewidth=1)
    steps(ax, sb.mean(h1_betti[lo:lo + half]), grid, color=colour, linewidth=3)
ax.set_xlim(grid[0], grid[-1])
ax.set_ylim(bottom=0)
save(fig, "betti-curves.svg")

# 4. Pairwise L1 distances between H1 stable ranks: two classes, two blocks.
dist = np.asarray(sb.pdist(h1_ranks, p=1))
fig, ax = figure()
ax.axis("off")
ax.imshow(dist, cmap=LinearSegmentedColormap.from_list("dist", [S1, S2, C["surface"]]),
          interpolation="nearest")
save(fig, "distances.svg")
