# stablebear-site

The StableBear landing page, served by GitHub Pages.

- `design/`: the design system (brand guide, tokens as JSON and CSS, `fonts.css` with the `@font-face` rules).
- `fonts/`: self-hosted Atkinson Hyperlegible Next and Mono and Inter Tight (`.woff2`), each with its SIL Open Font License (`OFL-*.txt`).
- `assets/logos/`: bear and head marks (SVG), lockups (PNG).
- `CLAUDE.md`: instructions Claude Code reads at the start of every session.

## Getting started

```sh
cd stablebear-site
git init && git add . && git commit -m "Design system and logos"
claude
```

A first prompt for Claude Code:

> Build index.html as a one-page landing site following CLAUDE.md and design/DESIGN.md: navbar with the head mark and the name, a hero with the bear mark and the tagline, an auto-advancing feature slideshow with dots, a `pip install stablebear` box with a copy button, feature cards, and a footer linking to the docs. Put styles in css/site.css and the slideshow in js/slideshow.js.

## Publishing

Push to GitHub, then Settings → Pages → deploy from the `main` branch, root folder. To serve it at stablebear.org, add a `CNAME` file containing `stablebear.org` and point the domain's DNS at GitHub Pages (currently stablebear.org redirects to the docs, so that redirect has to go).

## Licences

The fonts are Atkinson Hyperlegible Next and Mono (© The Atkinson Hyperlegible Project Authors) and Inter Tight (© The Inter Project Authors), all under the SIL Open Font License 1.1 (`fonts/OFL-*.txt`). The site's own code and the StableBear logos are under [YOUR LICENCE]; add a `LICENSE` file at the repo root for them.
