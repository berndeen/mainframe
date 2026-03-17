/**
 * Convert seconds to frames at given fps.
 */
export function secondsToFrames(seconds: number, fps: number): number {
  return Math.ceil(seconds * fps);
}

/**
 * Calculate total duration for a list of scene durations (in frames).
 */
export function totalDuration(sceneDurations: number[]): number {
  return sceneDurations.reduce((sum, d) => sum + d, 0);
}

/**
 * Calculate reading time in frames for a given text string.
 * Assumes ~200 words per minute reading speed.
 */
export function readingTimeFrames(text: string, fps: number): number {
  const words = text.split(/\s+/).length;
  const seconds = Math.max((words / 200) * 60, 2); // minimum 2 seconds
  return secondsToFrames(seconds, fps);
}
