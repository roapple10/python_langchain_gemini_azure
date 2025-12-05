import type { FocusSession } from './session'
import type { Tree } from './tree'

export interface UserPreferences {
  focusDurationMinutes: number
}

export interface StorageData {
  version: number
  sessions: FocusSession[]
  trees: Tree[]
  lastActiveSessionId: string | null
  userPreferences?: UserPreferences
}

export const STORAGE_KEY = 'forest-focus-data'
export const STORAGE_VERSION = 1
export const DEFAULT_FOCUS_DURATION_MINUTES = 25

