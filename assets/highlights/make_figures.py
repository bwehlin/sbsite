"""Generate the highlight banner figures (SVG, transparent, for the espresso band).

Run with stablebear 0.5.0 and matplotlib installed:
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
    ax.set_facecolor("none")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.set_xticks([])
    ax.set_yticks([])
    return fig, ax


def save(fig, name):
    fig.savefig(HERE / name, transparent=True, bbox_inches="tight", pad_inches=0.05,
                metadata={"Date": None})
    plt.close(fig)


def steps(ax, pcf, grid, **kw):
    ax.plot(grid, np.asarray(pcf(grid)).ravel(), drawstyle="steps-post", **kw)


# 1. Local topology at every point (data and settings from the relative subsampling tutorial).
# stablebear 0.5.0 has no subsample_relative yet, so the Gaussian-weighted draws
# (with replacement, duplicates discarded) are done here in NumPy.
np.random.seed(5)
centers = np.array([[-2.0, 0.0], [0.0, 0.0], [2.0, 0.0]])
clumps = np.vstack([
    0.13 * np.random.randn(10, 2) + [-0.8, -0.6],
    0.13 * np.random.randn(10, 2) + [-0.8, 0.6],
    0.13 * np.random.randn(10, 2) + [0.45, 0.0],
]) + centers[0]
blob = 0.9 * np.random.randn(120, 2) + centers[1]
ring = np.random.randn(120, 2)
ring = 1.1 * ring / np.linalg.norm(ring, axis=1, keepdims=True)
ring += 0.22 * np.random.randn(120, 2) + centers[2]
points = np.vstack([clumps, blob, ring]).astype(np.float32)

rng = np.random.default_rng(6)
n_samples, n_points, std = 100, 30, 0.5
d2 = ((points[:, None] - points[None]) ** 2).sum(-1)
weights = np.exp(-d2 / (2 * std**2))
weights /= weights.sum(1, keepdims=True)
samples = sb.zeros((len(points), n_samples), dtype=sb.pcloud32)
for q in range(len(points)):
    for s in range(n_samples):
        idx = np.unique(rng.choice(len(points), n_points, replace=True, p=weights[q]))
        samples[q, s] = points[idx]
ranks = persistence.barcode_to_stable_rank(
    persistence.compute_persistent_homology(samples, max_dim=0, reduced=True))
norms = np.asarray(sb.lp_norm(sb.mean(ranks, dim=1)[:, 0], p=1))

fig, ax = figure()
ax.axis("off")
# Low norms in deep gold, high norms in pale latte; clip the tails so the contrast reads.
cmap = LinearSegmentedColormap.from_list("band", [TOKENS_LIGHT["honey-ink"], S2, S1])
lo, hi = np.percentile(norms, [5, 95])
order = np.argsort(norms)
ax.scatter(*points[order].T, c=norms[order], cmap=cmap, vmin=lo, vmax=hi, s=30, linewidths=0)
ax.set_aspect("equal")
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
