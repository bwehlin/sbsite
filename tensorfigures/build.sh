#!/bin/sh
# Rebuild all data and figures from scratch.
set -e
PY="${PYTHON:-python3}"   # override with PYTHON=python if needed
cd "$(dirname "$0")"
mkdir -p data figures
"$PY" compute.py                 # StableBear: point clouds -> barcodes -> Betti curves
"$PY" fig_pointclouds.py         # figures/pointcloud-tensor-3x2.svg
"$PY" fig_barcodes.py            # figures/barcode-tensor-3x2x2.svg
"$PY" fig_barcodes.py --boxes    # figures/barcode-tensor-3x2x2-boxes.svg
"$PY" fig_betti.py               # figures/betti-tensor-3x2x2.svg
"$PY" render_png.py              # figures/*.png (needs Chrome/Chromium)
