export type SessionStatus = 'active' | 'paused' | 'completed' | 'abandoned'

export interface FocusSession {
  id: string
  startTime: number
  endTime: number | null
  status: SessionStatus
  remainingSeconds: number
  pausedAt: number | null
  totalPausedDuration: number
}

