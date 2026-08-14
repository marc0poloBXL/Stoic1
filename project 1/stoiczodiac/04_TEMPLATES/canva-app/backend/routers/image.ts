import express from "express";
import { generateImages } from "backend/services/image-generator";
import type { ImageResponse } from "backend/services/image-generator";

export type { ImageResponse };

export const createImageRouter = () => {
  const enum Routes {
    CREDITS = "/api/credits",
    PURCHASE_CREDITS = "/api/purchase-credits",
    QUEUE_IMAGE_GENERATION = "/api/queue-image-generation",
    JOB_STATUS = "/api/job-status",
    CANCEL_JOB = "/api/job-status/cancel",
  }

  const router = express.Router();

  // Jobs being processed: the promise settles when generation completes/errors
  const pendingJobs = new Map<
    string,
    { prompt: string; promise: Promise<ImageResponse[]> }
  >();
  const completedJobs = new Map<string, ImageResponse[]>();
  const failedJobs = new Map<string, string>();
  const cancelledJobs = new Set<string>();

  // Initial credit allocation for users, which decreases with each use.
  let credits = 10;
  const CREDITS_IN_BUNDLE = 10;

  /**
   * GET /api/credits — Returns the current credit balance.
   */
  router.get(Routes.CREDITS, async (_req, res) => {
    res.status(200).send({ credits });
  });

  /**
   * POST /api/purchase-credits — Adds a bundle of credits.
   */
  router.post(Routes.PURCHASE_CREDITS, async (_req, res) => {
    credits += CREDITS_IN_BUNDLE;
    res.status(200).send({ credits });
  });

  /**
   * GET /api/queue-image-generation?prompt=... — Kicks off a Leonardo AI generation job.
   */
  router.get(Routes.QUEUE_IMAGE_GENERATION, async (req, res) => {
    if (credits <= 0) {
      return res
        .status(403)
        .send("Not enough credits required to generate images.");
    }

    const prompt = req.query.prompt as string;
    const countParam = req.query.count as string | undefined;
    const numberOfImages = Math.min(Math.max(parseInt(countParam || "1", 10) || 1, 1), 4);

    if (!prompt) {
      return res.status(400).send("Missing prompt parameter.");
    }

    const jobId = generateJobId();

    // Start generation immediately (Leonardo AI or fallback)
    const promise = generateImages(prompt, numberOfImages)
      .then((images) => {
        pendingJobs.delete(jobId);
        // Mark as cancelled if the user cancelled while we were processing
        if (cancelledJobs.has(jobId)) {
          return images; // still stored so cancel endpoint can return them
        }
        completedJobs.set(jobId, images);
        credits -= 1;
        return images;
      })
      .catch((err: Error) => {
        pendingJobs.delete(jobId);
        failedJobs.set(jobId, err.message);
        throw err;
      });

    pendingJobs.set(jobId, { prompt, promise });

    return res.status(200).send({ jobId });
  });

  /**
   * GET /api/job-status?jobId=... — Returns the status of a generation job.
   * The frontend polls this endpoint. We also await the promise here so
   * the polling loop gets the result as soon as it's ready.
   */
  router.get(Routes.JOB_STATUS, async (req, res) => {
    const jobId = req.query.jobId as string;

    if (!jobId) {
      return res.status(400).send("Missing jobId parameter.");
    }

    // Completed
    const done = completedJobs.get(jobId);
    if (done) {
      return res.status(200).send({
        status: "completed",
        images: done,
        credits,
      });
    }

    // Cancelled
    if (cancelledJobs.has(jobId)) {
      const cancelledImages = completedJobs.get(jobId);
      return res.status(200).send({
        status: "cancelled",
        images: cancelledImages || [],
        credits,
      });
    }

    // Failed
    const errorMsg = failedJobs.get(jobId);
    if (errorMsg) {
      return res.status(200).send({
        status: "failed",
        error: errorMsg,
        credits,
      });
    }

    // Still pending — check if the promise has already settled (race condition safe)
    const pending = pendingJobs.get(jobId);
    if (pending) {
      // Race the promise against a short timeout so we don't block the response
      const result = await Promise.race([
        pending.promise.then(() => "done" as const),
        new Promise<"timeout">((resolve) => setTimeout(resolve, 500, "timeout")),
      ]);

      if (result === "done") {
        // Re-fetch from the completed/failed map (the .then handler above populated it)
        const images = completedJobs.get(jobId);
        if (images) {
          return res.status(200).send({ status: "completed", images, credits });
        }
        const err = failedJobs.get(jobId);
        return res.status(200).send({ status: "failed", error: err || "Unknown error", credits });
      }

      return res.status(200).send({ status: "processing" });
    }

    return res.status(404).send("Job not found.");
  });

  /**
   * POST /api/job-status/cancel?jobId=... — Cancels a pending generation job.
   */
  router.post(Routes.CANCEL_JOB, async (req, res) => {
    const jobId = req.query.jobId as string;

    if (!jobId) {
      return res.status(400).send("Missing jobId parameter.");
    }

    const pending = pendingJobs.get(jobId);
    if (pending) {
      cancelledJobs.add(jobId);
      pendingJobs.delete(jobId);
      return res.status(200).send("Job successfully cancelled.");
    }

    // Already completed or not found
    if (completedJobs.has(jobId) || failedJobs.has(jobId)) {
      return res.status(400).send("Job has already completed.");
    }

    return res.status(404).send("Job not found.");
  });

  /**
   * Generates a unique job ID.
   */
  function generateJobId(): string {
    return Math.random().toString(36).substring(2, 15);
  }

  return router;
};
