import type { FocusSession } from '../types/session'
import type { Tree } from '../types/tree'
import type { StorageData, UserPreferences } from '../types/storage'
import { STORAGE_VERSION, DEFAULT_FOCUS_DURATION_MINUTES } from '../types/storage'

const MAX_DURATION_SECONDS = 10800 // 180 minutes

/**
 * Validate FocusSession object
 */
export function validateSession(session: unknown): session is FocusSession {
  if (!session || typeof session !== 'object') return false

  const s = session as Record<string, unknown>

  return (
    typeof s.id === 'string' &&
    typeof s.startTime === 'number' &&
    (s.endTime === null || typeof s.endTime === 'number') &&
    ['active', 'paused', 'completed', 'abandoned'].includes(s.status as string) &&
    typeof s.remainingSeconds === 'number' &&
    s.remainingSeconds >= 0 &&
    s.remainingSeconds <= MAX_DURATION_SECONDS &&
    (s.pausedAt === null || typeof s.pausedAt === 'number') &&
    typeof s.totalPausedDuration === 'number' &&
    s.totalPausedDuration >= 0
  )
}

/**
 * Validate Tree object
 */
export function validateTree(tree: unknown): tree is Tree {
  if (!tree || typeof tree !== 'object') return false

  const t = tree as Record<string, unknown>

  return (
    typeof t.id === 'string' &&
    typeof t.completedAt === 'number' &&
    t.stage === 5 &&
    typeof t.date === 'string' &&
    /^\d{4}-\d{2}-\d{2}$/.test(t.date)
  )
}

/**
 * Validate UserPreferences object
 */
export function validateUserPreferences(prefs: unknown): prefs is UserPreferences {
  if (!prefs || typeof prefs !== 'object') return false

  const p = prefs as Record<string, unknown>

  return (
    typeof p.focusDurationMinutes === 'number' &&
    p.focusDurationMinutes >= 1 &&
    p.focusDurationMinutes <= 180 &&
    Number.isInteger(p.focusDurationMinutes)
  )
}

/**
 * Validate StorageData object
 */
export function validateData(data: unknown): data is StorageData {
  if (!data || typeof data !== 'object') return false

  const d = data as Record<string, unknown>

  if (
    typeof d.version !== 'number' ||
    !Array.isArray(d.sessions) ||
    !Array.isArray(d.trees) ||
    (d.lastActiveSessionId !== null && typeof d.lastActiveSessionId !== 'string')
  ) {
    return false
  }

  // Validate userPreferences if present
  if (d.userPreferences !== undefined && !validateUserPreferences(d.userPreferences)) {
    return false
  }

  // Validate all sessions
  for (const session of d.sessions) {
    if (!validateSession(session)) return false
  }

  // Validate all trees
  for (const tree of d.trees) {
    if (!validateTree(tree)) return false
  }

  return true
}

/**
 * Create empty StorageData
 */
export function createEmptyStorageData(): StorageData {
  return {
    version: STORAGE_VERSION,
    sessions: [],
    trees: [],
    lastActiveSessionId: null,
    userPreferences: {
      focusDurationMinutes: DEFAULT_FOCUS_DURATION_MINUTES,
    },
  }
}

