/**
 * Calculate remaining time from start time, duration, and pause duration
 * @param startTime - Timestamp when session started (ms)
 * @param durationSeconds - Total duration in seconds (1500 for 25 minutes)
 * @param totalPausedDuration - Total milliseconds paused
 * @returns Remaining seconds
 */
export function calculateRemaining(
  startTime: number,
  durationSeconds: number,
  totalPausedDuration: number
): number {
  const now = Date.now()
  const elapsed = now - startTime - totalPausedDuration
  const remaining = durationSeconds * 1000 - elapsed
  return Math.max(0, Math.floor(remaining / 1000))
}

/**
 * Check if timer is complete (reached 0)
 * @param remainingSeconds - Remaining time in seconds
 * @returns True if timer is complete
 */
export function isComplete(remainingSeconds: number): boolean {
  return remainingSeconds <= 0
}

