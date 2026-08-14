/**
 * Leonardo AI Image Generator Service
 *
 * Calls the Leonardo AI REST API to generate images from text prompts.
 * Falls back to placeholder images when no API key is set (dev-friendly).
 */
import debug from "debug";

const log = debug("server:image-generator");

const LEONARDO_API_BASE = "https://cloud.leonardo.ai/api/rest/v1";

// Leonardo Phoenix model (good all-purpose model for artistic/photorealistic)
const DEFAULT_MODEL_ID = "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3";

export interface ImageResponse {
  fullsize: { width: number; height: number; url: string };
  thumbnail: { width: number; height: number; url: string };
  label?: string;
}

interface LeonardoGenerationResponse {
  sdGenerationJob: {
    generationId: string;
  };
}

interface LeonardoJobStatusResponse {
  generations_by_pk: {
    status: "PENDING" | "COMPLETE" | "FAILED";
    generated_images: {
      id: string;
      url: string;
      width: number;
      height: number;
      nsfw: boolean;
    }[];
  };
}

/**
 * Placeholder images used when no API key is configured.
 */
const PLACEHOLDER_IMAGES: ImageResponse[] = [
  {
    fullsize: {
      width: 1280,
      height: 853,
      url: "https://images.pexels.com/photos/1145720/pexels-photo-1145720.jpeg?auto=compress&cs=tinysrgb&w=1280&h=853&dpr=2",
    },
    thumbnail: {
      width: 640,
      height: 427,
      url: "https://images.pexels.com/photos/1145720/pexels-photo-1145720.jpeg?auto=compress&cs=tinysrgb&w=640&h=427&dpr=2",
    },
  },
  {
    fullsize: {
      width: 1280,
      height: 853,
      url: "https://images.pexels.com/photos/4010108/pexels-photo-4010108.jpeg?auto=compress&cs=tinysrgb&w=1280&h=863&dpr=2",
    },
    thumbnail: {
      width: 640,
      height: 427,
      url: "https://images.pexels.com/photos/4010108/pexels-photo-4010108.jpeg?auto=compress&cs=tinysrgb&w=640&h=427&dpr=2",
    },
  },
  {
    fullsize: {
      width: 1280,
      height: 853,
      url: "https://images.pexels.com/photos/1327496/pexels-photo-1327496.jpeg?auto=compress&cs=tinysrgb&w=1280&h=853&dpr=2",
    },
    thumbnail: {
      width: 640,
      height: 427,
      url: "https://images.pexels.com/photos/1327496/pexels-photo-1327496.jpeg?auto=compress&cs=tinysrgb&w=640&h=427&dpr=2",
    },
  },
  {
    fullsize: {
      width: 1280,
      height: 853,
      url: "https://images.pexels.com/photos/4693135/pexels-photo-4693135.jpeg?auto=compress&cs=tinysrgb&w=1280&h=853&dpr=2",
    },
    thumbnail: {
      width: 640,
      height: 427,
      url: "https://images.pexels.com/photos/4693135/pexels-photo-4693135.jpeg?auto=compress&cs=tinysrgb&w=640&h=427&dpr=2",
    },
  },
];

/**
 * Returns true if a Leonardo API key is configured.
 */
function hasApiKey(): boolean {
  return !!(process.env.LEONARDO_API_KEY && process.env.LEONARDO_API_KEY.trim().length > 0);
}

/**
 * Start an image generation job on Leonardo AI.
 */
async function startGeneration(
  prompt: string,
  numberOfImages: number = 1,
): Promise<string> {
  const apiKey = process.env.LEONARDO_API_KEY!;

  const response = await fetch(`${LEONARDO_API_BASE}/generations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      prompt,
      modelId: DEFAULT_MODEL_ID,
      width: 1216,
      height: 832,
      num_images: Math.min(numberOfImages, 4), // Leonardo max 4 per job
      presetStyle: "CINEMATIC",
      alchemy: true,
      photoReal: false,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Leonardo API generation failed (${response.status}): ${errorText}`,
    );
  }

  const data = (await response.json()) as LeonardoGenerationResponse;
  log("Generation started: %s", data.sdGenerationJob.generationId);
  return data.sdGenerationJob.generationId;
}

/**
 * Poll a Leonardo generation job until it completes or fails.
 */
async function pollGeneration(
  generationId: string,
  maxAttempts: number = 30,
  intervalMs: number = 2000,
): Promise<ImageResponse[]> {
  const apiKey = process.env.LEONARDO_API_KEY!;

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const response = await fetch(
      `${LEONARDO_API_BASE}/generations/${generationId}`,
      {
        headers: {
          Authorization: `Bearer ${apiKey}`,
        },
      },
    );

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `Leonardo API poll failed (${response.status}): ${errorText}`,
      );
    }

    const data = (await response.json()) as LeonardoJobStatusResponse;
    const job = data.generations_by_pk;

    log(
      "Poll attempt %d/%d — status: %s",
      attempt + 1,
      maxAttempts,
      job.status,
    );

    if (job.status === "COMPLETE") {
      return job.generated_images
        .filter((img) => !img.nsfw)
        .map((img) => ({
          fullsize: {
            width: img.width || 1216,
            height: img.height || 832,
            url: img.url,
          },
          thumbnail: {
            width: Math.round((img.width || 1216) / 2),
            height: Math.round((img.height || 832) / 2),
            url: img.url, // Leonardo doesn't generate thumbnails separately
          },
        }));
    }

    if (job.status === "FAILED") {
      throw new Error("Leonardo generation failed");
    }

    // Still processing — wait and retry
    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }

  throw new Error("Leonardo generation timed out");
}

/**
 * Generate images from a text prompt using Leonardo AI.
 *
 * Returns real AI-generated images when LEONARDO_API_KEY is set,
 * or falls back to placeholder images for development.
 *
 * @param prompt - The text prompt for image generation
 * @param numberOfImages - How many images to generate (max 4)
 * @returns Array of ImageResponse objects with fullsize and thumbnail URLs
 */
export async function generateImages(
  prompt: string,
  numberOfImages: number = 1,
): Promise<ImageResponse[]> {
  if (!hasApiKey()) {
    log("No LEONARDO_API_KEY set — returning placeholder images");
    // Simulate processing delay for realistic UX
    await new Promise((resolve) => setTimeout(resolve, 3000));
    return PLACEHOLDER_IMAGES.slice(0, numberOfImages).map((img) => ({
      ...img,
      label: prompt,
    }));
  }

  try {
    const generationId = await startGeneration(prompt, numberOfImages);
    const images = await pollGeneration(generationId);
    return images.map((img) => ({ ...img, label: prompt }));
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);

    // Graceful fallback: if tokens are exhausted or API errors, return placeholders
    if (
      message.includes("not enough api tokens") ||
      message.includes("429") ||
      message.includes("insufficient_quota")
    ) {
      log(
        "Leonardo API token limit reached — falling back to placeholder images",
      );
      return PLACEHOLDER_IMAGES.slice(0, numberOfImages).map((img) => ({
        ...img,
        label: prompt,
      }));
    }

    // Re-throw other errors (auth failures, network issues, etc.)
    throw err;
  }
}