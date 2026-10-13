# stablebear-site

The StableBear landing page, built with Astro and served by GitHub Pages.

- `design/`: the design system (brand guide, tokens as JSON and CSS, `fonts.css` with the `@font-face` rules).
- `fonts/`: self-hosted Atkinson Hyperlegible Next and Mono and Inter Tight (`.woff2`), each with its SIL Open Font License (`OFL-*.txt`).
- `assets/logos/`: bear and head marks (SVG), lockups (PNG).
- `CLAUDE.md`: instructions Claude Code reads at the start of every session.

## Development

```sh
npm ci
npm run dev     # preview at http://localhost:4321/ (port 8000 in the devcontainer)
npm run build   # static site in dist/
```

- `src/pages/index.astro`: the landing page. `src/layouts/Base.astro`: head, navbar, footer. `src/components/`: widgets. `src/styles/site.css`: global styles.
- `assets/highlights/make_figures.py` regenerates the feature figures (needs `stablebear` and `matplotlib`).

## Publishing

`.github/workflows/deploy.yml` builds the site and deploys it to GitHub Pages on every push to `gh-pages`. One-time setup: Settings > Pages > Source: **GitHub Actions**. The site is then at https://stablebear.org (custom domain via `public/CNAME`).

To serve it at stablebear.org instead: add `public/CNAME` containing `stablebear.org`, set `site: "https://stablebear.org"` and remove `base` in `astro.config.mjs`, and point the domain's DNS at GitHub Pages (currently stablebear.org redirects to the docs, so that redirect has to go).

## Licences

The fonts are Atkinson Hyperlegible Next and Mono (© The Atkinson Hyperlegible Project Authors) and Inter Tight (© The Inter Project Authors), all under the SIL Open Font License 1.1 (`fonts/OFL-*.txt`). The site's own code and the StableBear logos are under [YOUR LICENCE]; add a `LICENSE` file at the repo root for them.
