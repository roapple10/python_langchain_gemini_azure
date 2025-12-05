import type { FocusSession } from '../types/session'

interface ControlsProps {
  session: FocusSession | null
  onStart: () => void
  onPause: () => void
  onResume: () => void
  onCancel: () => void
}

export function Controls({ session, onStart, onPause, onResume, onCancel }: ControlsProps) {
  if (!session) {
    return (
      <button
        className="btn btn-primary"
        onClick={onStart}
        aria-label="Start focus session"
      >
        Start Focus Session
      </button>
    )
  }

  if (session.status === 'paused') {
    return (
      <div className="timer-controls">
        <button
          className="btn btn-primary"
          onClick={onResume}
          aria-label="Resume timer"
        >
          Resume
        </button>
        <button
          className="btn btn-danger"
          onClick={onCancel}
          aria-label="Cancel session"
        >
          Cancel
        </button>
      </div>
    )
  }

  if (session.status === 'active') {
    return (
      <div className="timer-controls">
        <button
          className="btn btn-secondary"
          onClick={onPause}
          aria-label="Pause timer"
        >
          Pause
        </button>
        <button
          className="btn btn-danger"
          onClick={onCancel}
          aria-label="Cancel session"
        >
          Cancel
        </button>
      </div>
    )
  }

  return null
}

