import { defineConfig } from "astro/config";

// Served from GitHub Pages at https://bwehlin.github.io/sbsite/ (the dev server uses /sbsite/ too).
// When the site moves to stablebear.org, set site to "https://stablebear.org", drop base and
// add public/CNAME.
export default defineConfig({
  site: "https://bwehlin.github.io",
  base: "/sbsite",
});
