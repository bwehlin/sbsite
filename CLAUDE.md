# StableBear website

Landing page for StableBear, an open-source Python/C++/CUDA package for TDA on piecewise constant functions. Hosted on GitHub Pages. The documentation lives separately at https://docs.stablebear.org.

## Stack

- Astro (static output). Pages in `src/pages/`, the shared shell in `src/layouts/Base.astro`, widgets as components in `src/components/` (markup, data and their `<script>` together). Global styles in `src/styles/site.css`.
- `npm run dev` for the preview (port 8000 in the devcontainer), `npm run build` to check the static build in `dist/`.
- Reference local images and SVGs by importing them (`import x from "../../assets/..."`, then `x.src`) so any base path is applied; never hard-code `/assets/...` paths.
- `.github/workflows/deploy.yml` builds and deploys to GitHub Pages on every push to `gh-pages`.
- Prefer an existing, well-maintained component or library over hand-rolled widget JavaScript.

## Design rules (follow these on every change)

- Read `design/DESIGN.md` before designing anything: it is the brand guide (name, voice, colour roles, type, spacing, logo rules).
- Fonts are self-hosted: `src/layouts/Base.astro` imports `design/fonts.css` then `design/tokens.css`; every page uses that layout. Never load Google Fonts or any other font CDN. Keep the `fonts/OFL-*.txt` licences next to the font files.
- Text is Atkinson Hyperlegible Next (`--font-sans`), code is Atkinson Hyperlegible Mono (`--font-mono`), and the name StableBear is Inter Tight 800 (`--text-wordmark`, `--text-wordmark-nav`, letter-spacing `--wordmark-tracking`). Use Inter Tight for nothing else.
- Use only the CSS variables from `design/tokens.css` for colour, type, spacing and radii. No hard-coded hex values, font sizes or radii in page CSS.
- `design/tokens.css` is generated from `design/tokens.json`; never edit it by hand.
- The page is forced light (`data-theme="light"` on `<html>`). The dark-mode tokens stay in `design/tokens.css` for the docs.
- The name is `StableBear` in prose, headings, navigation and the logo; lowercase `stablebear` only in code, package names, commands and URLs.
- Logos are in `assets/logos/`. Prefer the SVG bear and head marks with the name set as text; the PNG lockups also work on light backgrounds.
- Text contrast at least 4.5:1 in both themes. Real buttons and links, visible focus states, works at phone width.
- Anything that moves on its own pauses on hover/focus, has a pause button, and starts paused under `prefers-reduced-motion`.

## Content

- Use only facts from the docs site or ones I give you. No invented features, numbers or API names; mark unknowns as `[PLACEHOLDER]`.
