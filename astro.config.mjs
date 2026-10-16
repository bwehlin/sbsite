import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// Served from GitHub Pages at https://stablebear.org (custom domain, see public/CNAME).
export default defineConfig({
  site: "https://stablebear.org",
  integrations: [sitemap()],
});
