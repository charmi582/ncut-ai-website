import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const outDir = join(root, "dist");

const files = [
  "404.html",
  "awards.html",
  "campus-links.html",
  "faculty-detail.html",
  "faculty.html",
  "index.html",
  "manifest.webmanifest",
  "news-detail.html",
  "news.html",
  "official-detail.html",
  "official.html",
  "original.html",
  "page.html",
  "resources.html",
  "robots.txt",
  "script.js",
  "sitemap.xml",
  "student-resource.html",
  "styles.css"
];

const directories = [
  "assets",
  "data"
];

const jsonFiles = [
  "data/site.json",
  "data/official-pages.json",
  "manifest.webmanifest"
];

function stripBom(text) {
  return text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
}

async function copyFilePreservingPath(file) {
  const source = join(root, file);
  const target = join(outDir, file);
  await mkdir(dirname(target), { recursive: true });
  await cp(source, target);
}

async function copyDirectory(directory) {
  await cp(join(root, directory), join(outDir, directory), {
    recursive: true,
    filter: (source) => !source.includes(`${directory}\\backups`) && !source.includes(`${directory}/backups`)
  });
}

async function normalizeJson(file) {
  const target = join(outDir, file);
  const text = stripBom(await readFile(target, "utf8"));
  JSON.parse(text);
  await writeFile(target, text, "utf8");
}

await rm(outDir, { recursive: true, force: true });
await mkdir(outDir, { recursive: true });

for (const file of files) {
  await copyFilePreservingPath(file);
}

for (const directory of directories) {
  await copyDirectory(directory);
}

for (const file of jsonFiles) {
  await normalizeJson(file);
}

await writeFile(join(outDir, ".nojekyll"), "", "utf8");

console.log(`GitHub Pages static build written to ${outDir}`);
