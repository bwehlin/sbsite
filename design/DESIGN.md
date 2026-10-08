# StableBear

A computational package for discrete objects in Python and C++.

StableBear is an open-source Python package with a C++/CUDA backend for GPU-accelerated computation on piecewise constant functions: stable ranks, Euler characteristic curves, Betti curves and the distances and kernels between them. This system is the visual language for its website, documentation and teaching material. It is a deliberately small first version, built from the docs site (PyData Sphinx theme, light and dark modes) and the package's own subject matter; the logo and the bear's colour come from the official artwork.

## Content fundamentals

- **Name.** `StableBear` in prose, headings, navigation and the logo: one word, capital S and B. Never "Stablebear", "Stable Bear" or lowercase "stablebear" in running text. In code, package names, commands and URLs it is lowercase, as Python requires: `pip install stablebear`, `import stablebear as sb`, docs.stablebear.org.
- **Voice.** Precise, plain and mathematical. Say what a function computes and on what objects ("computes pairwise L_p distances between stable rank curves"), not how exciting it is. Avoid marketing adjectives.
- **Audience.** TDA practitioners and students. Assume NumPy fluency; define TDA terms on first use and link to the docs.
- **Code first.** Every concept page leads with a short runnable example, then explains it.

## Visual foundations

- **Step functions are the motif.** The package is about piecewise constant functions, so the identity is built from flat bars and sharp steps: rectangles with `radius-sm` corners, horizontal rules, no curves or blobs.
- **Colour.** `fur` (the bear) and black are what people know StableBear by: use `fur` for big fills and callout bands (`fur-tint` for softer ones), never for text. Place the bear on the plain page surface, not on a `fur` or `fur-tint` panel: beige on beige weakens it. `espresso` is the brand and interactive colour: a dark coffee brown in light mode and a pale latte in dark mode, for links, primary buttons, focus rings, solid bands and the first series in plots, with `on-espresso` text on it and `espresso-tint` for soft fills. It sits tone-on-tone with the bear, so the palette reads warm and quiet. `honey` is the gold accent: second plot series, step markers, highlight badges, always with dark text on it; `honey-ink` when it is small text. `danger` means errors, deprecations and destructive actions only. Everything else is `surface`, `ink`, `ink-muted` and `border`.
- **Plots.** Series 1 `espresso`, series 2 `honey`, series 3 `ink-muted`. Draw step functions with `drawstyle="steps-post"`, never interpolated lines. These differ in lightness as well as hue, so they still read in greyscale.
- **Type.** Three free families, all under the SIL Open Font License 1.1. **Atkinson Hyperlegible Next** sets all text: body, headings (weight 700), navigation and buttons; `body` is 16/26 for long-form docs. **Atkinson Hyperlegible Mono** sets code and identifiers. **Inter Tight** ExtraBold (800, letter-spacing −0.035em) sets only the name StableBear (the `wordmark` styles), echoing the logo's heavy grotesk. Atkinson has no Greek letters, subscript digits or arrows, so Inter Tight sits second in the text stack and supplies ε, δ, H₀, → and the like; typeset real formulas with MathJax or KaTeX. Self-host the `.woff2` files in `fonts/` with their `OFL-*.txt` licences beside them; never load them from Google Fonts, so no visitor data goes to a third party.
- **Space and shape.** A 4px base: `space-1` 4, `space-2` 8, `space-4` 16, `space-8` 32. Radii stay small (`radius-sm` 2, `radius-md` 4, `radius-lg` 8); nothing is pill-shaped.
- **Borders, not shadows.** Separate regions with `border` hairlines and `surface-raised` / `surface-sunken`, not drop shadows.
- **Dark mode is first-class.** Every token has a dark value, and dark surfaces are warm brown-blacks, not cool greys; check both themes for each new page.

## Logo

Two lockups and two marks, all in the **Logos** group:

- **Horizontal lockup** (PNG): wordmark left, the bear sitting cross-legged with arms open. Site headers, slides, banners.
- **Stacked lockup** (PNG): the bear's head over the wordmark. Square spaces with room for the name: social cards, title slides.
- **Bear mark** (SVG): the full-body bear alone. Hero areas, the docs landing page, beside a name already set in text.
- **Head mark** (SVG): the head alone. Navbar icon, favicon, avatars, anywhere small.

Rules:

- The artwork is `fur` with `logo-ink` black outlines on a transparent background. Prefer the SVGs wherever the format allows; they stay sharp at every size.
- **On light surfaces** (`surface`, `surface-raised`, white) any of the four works.
- **On dark surfaces** use the bear or head mark: the `fur` fill carries the shape, so they read without changes. The lockups' black wordmark disappears there; in dark mode, set the name next to a mark in text instead (Inter Tight 800, `ink`), or put the lockup on a light plate (light-theme `surface`, `radius-lg` corners, `space-4` padding).
- Keep clear space of at least the height of the wordmark's "S" (for the marks, a quarter of the mark's width) on all sides. Don't recolour, outline, stretch, rotate or redraw the bear.
- The lockups' wordmark spells "StableBear", matching the name. Where the name is set as text next to a mark, use `StableBear` in Inter Tight 800, `ink`, letter-spacing −0.035em.

## Iconography

No icon set yet. In docs, use the PyData Sphinx theme's default icons and don't add decorative ones. The bear is the brand's only illustration; don't draw new bears or other mascots.
