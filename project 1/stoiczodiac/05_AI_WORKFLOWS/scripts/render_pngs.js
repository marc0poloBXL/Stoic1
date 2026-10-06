/**
 * Convert SVG designs to ready-to-post PNGs.
 * Fixes the "too small / horizontal" issue — PNGs are exactly 1080×1080 or 1080×1920.
 * Uses sharp (available via Next.js dependency).
 */
const fs = require("fs");
const path = require("path");

async function main() {
  const sharp = (await import("sharp")).default;

  const weekArg = process.argv.find((a) => a.startsWith("--week="));
  const weekFolder = weekArg ? weekArg.split("=")[1] : "week_20260907";

  const weekDir = path.resolve(
    __dirname,
    `../../11_MEDIA_LIBRARY/SCHEDULED/${weekFolder}`
  );

  // Process each folder
  const jobs = [
    { dir: "quotes", ext: ".svg", width: 1080, height: 1080 },
    { dir: "stories", ext: ".svg", width: 1080, height: 1920 },
  ];

  for (const job of jobs) {
    const srcDir = path.join(weekDir, job.dir);
    const outDir = path.join(weekDir, job.dir + "_png");
    fs.mkdirSync(outDir, { recursive: true });

    const files = fs.readdirSync(srcDir).filter((f) => f.endsWith(job.ext));
    for (const file of files) {
      const svgPath = path.join(srcDir, file);
      let svg = fs.readFileSync(svgPath, "utf8");

      // Replace fonts with Windows-safe fallbacks
      // Playfair Display → Georgia, Raleway → Arial, Cormorant Garamond → 'Times New Roman'
      svg = svg
        .replace(/font-family="'Playfair Display', Georgia, serif"/g, 'font-family="Georgia, serif"')
        .replace(/font-family="Playfair Display',Georgia,serif"/g, 'font-family="Georgia, serif"')
        .replace(/font-family="'Playfair Display',Georgia,serif"/g, 'font-family="Georgia, serif"')
        .replace(/font-family="'Cormorant Garamond', 'Times New Roman', serif"/g, 'font-family="Georgia, serif"')
        .replace(/font-family="Raleway, 'Helvetica Neue', sans-serif"/g, 'font-family="Arial, sans-serif"')
        .replace(/font-family="Raleway, sans-serif"/g, 'font-family="Arial, sans-serif"')
        .replace(/font-family="Raleway,sans-serif"/g, 'font-family="Arial, sans-serif"')
        .replace(/font-family="serif"/g, 'font-family="Georgia, serif"')
        .replace(/font-family="'Raleway', 'Helvetica Neue', sans-serif"/g, 'font-family="Arial, sans-serif"');

      // Remove SVG filters that sharp/librsvg can't handle (marble texture, glow)
      svg = svg.replace(/<filter id="marble">[\s\S]*?<\/filter>/g, "");
      svg = svg.replace(/<filter id="textGlow">[\s\S]*?<\/filter>/g, "");
      svg = svg.replace(/<filter id="textShadow">[\s\S]*?<\/filter>/g, "");
      svg = svg.replace(/<filter id="glow">[\s\S]*?<\/filter>/g, "");
      // Remove filter references
      svg = svg.replace(/ filter="url\(#marble\)"/g, "");
      svg = svg.replace(/ filter="url\(#textGlow\)"/g, "");
      svg = svg.replace(/ filter="url\(#textShadow\)"/g, "");
      svg = svg.replace(/ filter="url\(#glow\)"/g, "");

      const pngName = file.replace(/\.svg$/i, ".png");
      const pngPath = path.join(outDir, pngName);

      try {
        await sharp(Buffer.from(svg))
          .resize(job.width, job.height)
          .png()
          .toFile(pngPath);
        console.log(`  ✓ ${job.dir}/${pngName}`);
      } catch (err) {
        console.error(`  ✗ ${job.dir}/${pngName}: ${err.message}`);
      }
    }
  }

  // Also process carousel slides
  const carouselDir = path.join(weekDir, "carousels");
  if (fs.existsSync(carouselDir)) {
    const outDir = path.join(weekDir, "carousels_png");
    fs.mkdirSync(outDir, { recursive: true });

    const spotlightDirs = fs.readdirSync(carouselDir).filter((d) =>
      fs.statSync(path.join(carouselDir, d)).isDirectory()
    );
    for (const sd of spotlightDirs) {
      const slides = fs
        .readdirSync(path.join(carouselDir, sd))
        .filter((f) => f.endsWith(".svg"))
        .sort();
      const spotOutDir = path.join(outDir, sd);
      fs.mkdirSync(spotOutDir, { recursive: true });

      for (const slide of slides) {
        let svg = fs.readFileSync(path.join(carouselDir, sd, slide), "utf8");
        svg = svg
          .replace(/font-family="'Playfair Display', Georgia, serif"/g, 'font-family="Georgia, serif"')
          .replace(/font-family="Playfair Display',Georgia,serif"/g, 'font-family="Georgia, serif"')
          .replace(/font-family="'Playfair Display',Georgia,serif"/g, 'font-family="Georgia, serif"')
          .replace(/font-family="Raleway, 'Helvetica Neue', sans-serif"/g, 'font-family="Arial, sans-serif"')
          .replace(/font-family="Raleway, sans-serif"/g, 'font-family="Arial, sans-serif"')
          .replace(/font-family="Raleway,sans-serif"/g, 'font-family="Arial, sans-serif"')
          .replace(/font-family="serif"/g, 'font-family="Georgia, serif"')
          .replace(/<filter id="marble">[\s\S]*?<\/filter>/g, "")
          .replace(/<filter id="glow">[\s\S]*?<\/filter>/g, "")
          .replace(/ filter="url\(#marble\)"/g, "")
          .replace(/ filter="url\(#glow\)"/g, "");
        const pngName = slide.replace(/\.svg$/i, ".png");
        try {
          await sharp(Buffer.from(svg))
            .resize(1080, 1080)
            .png()
            .toFile(path.join(spotOutDir, pngName));
          console.log(`  ✓ carousels/${sd}/${pngName}`);
        } catch (err) {
          console.error(`  ✗ carousels/${sd}/${pngName}: ${err.message}`);
        }
      }
    }
  }

  console.log("\n✅ All PNGs generated!");
}

main().catch(console.error);