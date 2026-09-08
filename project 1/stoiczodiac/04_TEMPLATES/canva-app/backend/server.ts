import { config } from "dotenv";
import cors from "cors";
import express from "express";

// Load .env so the backend process sees LEONARDO_API_KEY and others
config();

const LEONARDO_BASE = "https://cloud.leonardo.ai/api/rest/v1";
const LEONARDO_API_KEY = process.env.LEONARDO_API_KEY;
const LEONARDO_MODEL_ID =
  process.env.LEONARDO_MODEL_ID || "de7d3faf-762f-48e0-b3b7-9d0ac3a3fcf3"; // Phoenix 1.0

const PORT = process.env.CANVA_BACKEND_PORT || 3001;

if (!LEONARDO_API_KEY) {
  console.error(
    "❌ LEONARDO_API_KEY is not set in the environment. " +
      "Add it to your .env file: LEONARDO_API_KEY=your_key_here",
  );
  process.exit(1);
}

const app = express();
app.use(cors());
app.use(express.json());

// ---------------------------------------------------------------------------
// Helper: call Leonardo AI API
// ---------------------------------------------------------------------------
async function leonardoFetch<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const url = `${LEONARDO_BASE}${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      accept: "application/json",
      authorization: `Bearer ${LEONARDO_API_KEY}`,
      "content-type": "application/json",
      ...(options.headers as Record<string, string> | undefined),
    },
  });

  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(
      `Leonardo API error ${res.status} for ${options.method || "GET"} ${path}: ${body}`,
    );
  }

  return (await res.json()) as T;
}

// ---------------------------------------------------------------------------
// GET /api/credits — return remaining Leonardo tokens
// ---------------------------------------------------------------------------
app.get("/api/credits", async (_req, res) => {
  try {
    const data = await leonardoFetch<{
      user_details: Array<{
        subscriptionTokens?: number | null;
        subscriptionGptTokens?: number | null;
        subscriptionModelTokens?: number | null;
        paidTokens?: number | null;
        apiSubscriptionTokens?: number | null;
        apiPaidTokens?: number | null;
        apiConcurrencySlots?: number | null;
        apiPlanTokenRenewalDate?: string | null;
        tokenRenewalDate?: string | null;
      }>;
    }>("/me");

    const details = data.user_details[0];

    // Leonardo returns credit balances in multiple fields.
    // API users get apiPaidTokens and/or apiSubscriptionTokens.
    // Free/web users get subscriptionTokens + paidTokens.
    const apiTokens = details?.apiSubscriptionTokens ?? 0;
    const apiPaid = details?.apiPaidTokens ?? 0;
    const subscriptionTokens = details?.subscriptionTokens ?? 0;
    const paidTokens = details?.paidTokens ?? 0;

    // Use API token balance when present; fall back to subscription tokens.
    const credits =
      apiTokens + apiPaid > 0
        ? apiTokens + apiPaid
        : subscriptionTokens + paidTokens;

    res.json({ credits });
  } catch (err) {
    console.error("Failed to fetch credits:", err);
    // Return a default so the UI doesn't completely break
    res.json({ credits: 150 });
  }
});

// ---------------------------------------------------------------------------
// POST /api/queue-image-generation — kick off a Leonardo generation
// ---------------------------------------------------------------------------
app.post("/api/queue-image-generation", async (req, res) => {
  try {
    const { prompt, count: numImages } = req.query;
    const num = Math.min(Math.max(Number(numImages) || 1, 1), 8);

    const body: Record<string, unknown> = {
      modelId: LEONARDO_MODEL_ID,
      prompt: String(prompt || ""),
      num_images: num,
      width: 1024,
      height: 1024,
      alchemy: true,
      contrast: 3.5,
      enhancePrompt: false,
    };

    // Apply style preset if one was sent from the frontend
    const styleUuid = req.body?.styleUuid;
    if (styleUuid) {
      body.styleUUID = styleUuid;
    }

    const data = await leonardoFetch<{
      sdGenerationJob: { generationId: string };
    }>("/generations", {
      method: "POST",
      body: JSON.stringify(body),
    });

    const jobId = data.sdGenerationJob.generationId;
    res.json({ jobId });
  } catch (err) {
    console.error("Failed to queue generation:", err);
    res.status(500).json({ error: "Failed to queue image generation" });
  }
});

// ---------------------------------------------------------------------------
// GET /api/job-status — poll for generation completion
// ---------------------------------------------------------------------------
app.get("/api/job-status", async (req, res) => {
  try {
    const jobId = req.query.jobId as string;
    if (!jobId) {
      res.status(400).json({ error: "Missing jobId query parameter" });
      return;
    }

    const data = await leonardoFetch<{
      generations_by_pk: {
        status: "COMPLETE" | "PENDING" | "FAILED";
        generated_images?: Array<{
          url: string;
          width: number;
          height: number;
          nsfw: boolean;
        }>;
      };
    }>(`/generations/${jobId}`);

    const job = data.generations_by_pk;

    if (job.status === "COMPLETE") {
      const images = (job.generated_images ?? [])
        .filter((img) => !img.nsfw)
        .map((img, i) => ({
          label: `Generated image ${i + 1}`,
          fullsize: { width: img.width, height: img.height, url: img.url },
          thumbnail: { width: 256, height: 256, url: img.url },
        }));

      res.json({
        status: "completed",
        images,
        credits: 1, // will be refreshed on the next credits call
      });
    } else if (job.status === "FAILED") {
      res.json({ status: "cancelled", images: [], credits: 0 });
    } else {
      res.json({ status: "processing", images: [], credits: 0 });
    }
  } catch (err) {
    console.error("Failed to check job status:", err);
    res.status(500).json({ error: "Failed to check job status" });
  }
});

// ---------------------------------------------------------------------------
// POST /api/job-status/cancel — cancel a running generation
// ---------------------------------------------------------------------------
app.post("/api/job-status/cancel", async (req, res) => {
  try {
    const jobId = req.query.jobId as string;
    if (!jobId) {
      res.status(400).json({ error: "Missing jobId query parameter" });
      return;
    }

    // Leonardo supports DELETE /generations/{id} to cancel
    await leonardoFetch(`/generations/${jobId}`, { method: "DELETE" });
    res.json({ success: true });
  } catch (err) {
    console.error("Failed to cancel job:", err);
    // If the job is already done, that's fine
    res.json({ success: true });
  }
});

// ---------------------------------------------------------------------------
// POST /api/purchase-credits — redirect to Leonardo subscription page
// ---------------------------------------------------------------------------
app.post("/api/purchase-credits", async (_req, res) => {
  // Leonardo doesn't have a purchase API — redirect to their billing page
  res.json({ url: "https://leonardo.ai/subscription" });
});

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------
app.listen(PORT, () => {
  console.log(`\n  🏛️  Stoic Zodiac Backend — listening on port ${PORT}`);
  console.log(`  🎨 Leonardo AI (Phoenix 1.0) — model: ${LEONARDO_MODEL_ID}`);
  console.log(`  🔑 API key: ${LEONARDO_API_KEY ? "✓ configured" : "✗ missing"}\n`);
});