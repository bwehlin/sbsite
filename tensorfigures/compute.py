"""Compute the data behind figures 2 and 3 with StableBear.

point clouds, shape (3, 2)
  -> compute_persistent_homology(max_dim=1)  -> BarcodeTensor, shape (3, 2, 2)
  -> barcode_to_betti_curve                  -> PcfTensor,     shape (3, 2, 2)

Writes data/barcodes.json and data/betti_curves.json, keyed "ijk"
(row i, column j, homology degree k).
"""
import json
import numpy as np
import stablebear as sb
from stablebear.persistence import compute_persistent_homology, barcode_to_betti_curve

from clouds import cells

X = sb.zeros((3, 2), dtype=sb.pcloud64)
for i in range(3):
    for j in range(2):
        X[i, j] = np.ascontiguousarray(cells[i][j][0], dtype=np.float64)

barcodes = compute_persistent_homology(X, max_dim=1)   # shape (3, 2, 2)
betti = barcode_to_betti_curve(barcodes)               # shape (3, 2, 2)

bars_out, betti_out = {}, {}
for i in range(3):
    for j in range(2):
        for k in range(2):
            key = f"{i}{j}{k}"
            bars_out[key] = barcodes[i, j, k].to_numpy().tolist()   # rows (birth, death); death may be inf
            betti_out[key] = betti[i, j, k].to_numpy().tolist()     # rows (t, value) of a step function

json.dump(bars_out, open("data/barcodes.json", "w"))
json.dump(betti_out, open("data/betti_curves.json", "w"))
print("barcodes:", barcodes.shape, " betti curves:", betti.shape)
