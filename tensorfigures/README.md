# StableBear tensor figures

Three illustrations of StableBear tensors, drawn as blocks of glass cells. They form one pipeline on the same six point clouds:

| Figure | Tensor | Shape | Contents |
|---|---|---|---|
| `figures/pointcloud-tensor-3x2.svg` | `PointCloudTensor` | (3, 2) | circle, torus, sphere, three clusters, helix, uniform noise |
| `figures/barcode-tensor-3x2x2.svg` (and `-boxes.svg`) | `BarcodeTensor` | (3, 2, 2) | `compute_persistent_homology(X, max_dim=1)`; H₁ in front, H₀ behind |
| `figures/betti-tensor-3x2x2.svg` | `PcfTensor` | (3, 2, 2) | `barcode_to_betti_curve` of the barcodes; H₁ in front, H₀ behind |

Each figure comes as an SVG for the web and a 3× PNG with a transparent background for slides.

## Rebuild

```sh
pip install -r requirements.txt
sh build.sh        # uses python3; set PYTHON=... to use another interpreter
```

`build.sh` runs, in order:

1. `compute.py`: computes the barcodes and Betti curves with StableBear and saves them to `data/`.
2. `fig_pointclouds.py`, `fig_barcodes.py` (with `--boxes` for the 3D-box variant) and `fig_betti.py`: write the SVGs to `figures/`.
3. `render_png.py`: renders the PNGs with headless Chrome/Chromium (set `CHROME=/path/to/chrome` if needed).

The point clouds are defined in `clouds.py` with a fixed random seed, so every run gives the same figures.

## Drawing conventions

- **Projection:** cabinet-style oblique, with depth drawn up and to the right. Each figure's look is set by `S` (cell size in px), `K` (depth scale) and `A` (depth angle) at the top of its script.
- **Centring:** each cloud, barcode and curve is centred on the front face of its own cell, which reads as centred; centring on the 3D middle looks shifted up and right.
- **Simplifications in the barcode figure:** at most the 16 longest H₀ bars and 6 longest H₁ bars per cell; very short H₁ noise bars are dropped, keeping at least three.
- **Scale:** each barcode and Betti curve is scaled to its own cell, so lengths and heights can't be compared between cells.
- **Colours:** H₁ is espresso (`--sb-h1`), H₀ is faint honey (`--sb-h0`) and the glass is `fur`.

## Using the SVGs on the site

The SVGs read the design system's CSS variables (`--ink`, `--espresso`, `--honey`, `--fur`) when inlined in a page, and follow `prefers-color-scheme` for dark mode. Opened on their own, or used through an `<img>` tag, they fall back to the built-in light colours. They use CSS `color-mix()`, which all current browsers support.

Each SVG has a `<title>` and `<desc>` for screen readers.
