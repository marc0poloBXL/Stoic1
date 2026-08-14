import { user } from "@canva/app-middleware/express";
import cors from "cors";
import express from "express";
import { createBaseServer } from "utils/backend/base_backend/create";
import { createImageRouter } from "./routers/image";
import { generateImages } from "backend/services/image-generator";

async function main() {
  const APP_ID = process.env.CANVA_APP_ID;

  if (!APP_ID) {
    throw new Error(
      `The CANVA_APP_ID environment variable is undefined. Set the variable in the project's .env file.`,
    );
  }

  const router = express.Router();

  router.use(cors());

  /**
   * Dev/test endpoint — bypasses JWT auth for easy curl testing.
   * Only exposed when LEONARDO_API_KEY is set AND NODE_ENV is not 'production'.
   * Usage: GET /api/test/generate?prompt=...
   */
  if (process.env.LEONARDO_API_KEY && process.env.NODE_ENV !== "production") {
    router.get("/api/test/generate", async (req, res) => {
      const prompt = req.query.prompt as string;
      if (!prompt) {
        return res.status(400).send("Missing prompt parameter.");
      }
      try {
        const images = await generateImages(prompt, 1);
        res.status(200).json({ status: "completed", images });
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : String(err);
        res.status(500).json({ status: "failed", error: message });
      }
    });
    console.log("🔬 Dev test endpoint enabled: GET /api/test/generate?prompt=...");
  }

  /**
   * Initialize JWT middleware to verify Canva user tokens
   */
  router.use(user.verifyToken({ appId: APP_ID }));

  /**
   * Add routes for image generation.
   */
  const imageRouter = createImageRouter();
  router.use(imageRouter);

  const server = createBaseServer(router);
  server.start(process.env.CANVA_BACKEND_PORT);
}

main();
