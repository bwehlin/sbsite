---
title: StableBear 0.5.1 released
tag: Release
summary: Relative subsampling, Python 3.15 support and wheels for Windows on ARM64.
---

- **Relative subsampling:** `random.subsample_relative` draws from a point cloud or distance matrix with probabilities weighted by distance to query points, using the new Gaussian, Uniform and Mixture weights. See the [tutorial](https://docs.stablebear.org/en/stable/tutorial_notebooks/relative_subsampling.html).
- **Python 3.15:** wheels for CPython 3.15, including the free-threaded build.
- **Windows on ARM64:** CPU-only wheels for Python 3.11 and newer.

This release changes the `random.subsample` defaults and the results for a given seed. See the [changelog](https://docs.stablebear.org/en/stable/changelog.html) for all changes.
