/**
 * Format seconds to MM:SS string
 * @param seconds - Total seconds (0-3600)
 * @returns Formatted time string (e.g., "25:00", "05:30", "00:45")
 */
export function formatTime(seconds: number): string {
  if (seconds < 0) return '00:00'
  if (seconds > 3600) return '60:00'

  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60

  return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
}

