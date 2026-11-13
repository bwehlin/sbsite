---
title: StableBear 0.6.0 released
date: 2026-11-11
tag: Release
summary: Time series support, with time delay embedding and windowing.
---

The headline of this release is time series. `timeseries.TimeSeries` holds observations of any element type at numeric, duration or date timestamps, and comes with the tools to take a series to persistent homology:

- `cut_windows` cuts a series into windows.
- `delay_embed` builds delay embeddings.
- `to_point_clouds` turns a series into point clouds.
- `plotting.plot_timeseries` draws a series.

The release also makes GPU and parallel computations sturdier and has a few breaking changes, to `allclose`, `bool()` on tensors and `point_process.sample_poisson`. See the [changelog](https://docs.stablebear.org/en/stable/changelog.html) for all changes.
