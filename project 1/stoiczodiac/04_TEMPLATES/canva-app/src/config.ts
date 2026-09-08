/**
 * Expected loading time for the progress bar.
 * Adjust this value to match the estimated loading time of your Generative AI model.
 */
export const EXPECTED_LOADING_TIME_IN_SECONDS = 5;

/**
 * Determines the default number of images generated when using the `generateImages` function.
 */
export const NUMBER_OF_IMAGES_TO_GENERATE = 4;

/**
 * Number of seconds to wait between polling for generated images.
 */
export const POLLING_INTERVAL_IN_SECONDS = 3;

/**
 * Maximum number of polling attempts before giving up on a generation job.
 * At 3s per interval this gives a ~60s timeout, which accommodates
 * Leonardo AI generation times of 15–45s with margin for queue delays.
 */
export const MAX_POLLING_ATTEMPTS = 20;

/**
 * Your app's name. This is used when reporting generated content.
 */
export const APP_NAME = "Stoic Zodiac";

/**
 * The link that will open when a user needs to buy more credits.
 * Update this when you set up a credit purchase page (e.g. a Leonardo AI
 * subscription link, a Gumroad upsell, or a Canva app purchase flow).
 * @TODO: Replace with your actual credit purchase URL.
 */
export const PURCHASE_URL = "https://leonardo.ai/subscription";
