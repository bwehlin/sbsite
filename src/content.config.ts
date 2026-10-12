import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

// News items: one Markdown file each. The summary is the short highlight on the home page,
// the body the full item on the news page.
const news = defineCollection({
  loader: glob({ base: "./src/content/news", pattern: "*.md" }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date().optional(),
    summary: z.string(),
    // Short label shown as a badge, such as "Release".
    tag: z.string().optional(),
  }),
});

export const collections = { news };
