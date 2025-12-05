import { formatTime } from '../utils/time'

interface TimerProps {
  remainingSeconds: number
  durationSeconds: number
  isPaused: boolean
  onPause: () => void
  onResume: () => void
  onCancel: () => void
  onStart: () => void
}

export function Timer({
  remainingSeconds,
  durationSeconds,
  isPaused,
  onPause,
  onResume,
  onCancel,
  onStart,
}: TimerProps) {
  const timeString = formatTime(remainingSeconds)
  const hasActiveSession = remainingSeconds < durationSeconds && remainingSeconds > 0

  return (
    <div className="timer-container">
      <div
        className="timer-display"
        role="timer"
        aria-label={`Timer: ${timeString} remaining`}
        aria-live="polite"
        aria-atomic="true"
      >
        {timeString}
      </div>

      {!hasActiveSession && (
        <button
          className="btn btn-primary"
          onClick={onStart}
          aria-label="Start focus session"
        >
          Start Focus Session
        </button>
      )}

      {hasActiveSession && (
        <div className="timer-controls">
          {isPaused ? (
            <button
              className="btn btn-primary"
              onClick={onResume}
              aria-label="Resume timer"
            >
              Resume
            </button>
          ) : (
            <button
              className="btn btn-secondary"
              onClick={onPause}
              aria-label="Pause timer"
            >
              Pause
            </button>
          )}
          <button
            className="btn btn-danger"
            onClick={onCancel}
            aria-label="Cancel session"
          >
            Cancel
          </button>
        </div>
      )}
    </div>
  )
}

