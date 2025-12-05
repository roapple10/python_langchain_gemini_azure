import type { StorageData } from '../types/storage'
import { STORAGE_KEY, STORAGE_VERSION } from '../types/storage'
import { validateData, createEmptyStorageData } from '../utils/validation'

/**
 * Load data from localStorage
 * @returns StorageData or null if not found/invalid
 */
export function loadData(): StorageData | null {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return null

    const data = JSON.parse(stored) as unknown

    if (validateData(data)) {
      // Handle version migration if needed
      if (data.version !== STORAGE_VERSION) {
        // Future: implement migration logic here
        console.warn(`Storage version mismatch: ${data.version} vs ${STORAGE_VERSION}`)
      }
      return data
    }

    console.error('Invalid storage data format')
    return null
  } catch (error) {
    console.error('Error loading storage data:', error)
    return null
  }
}

/**
 * Save data to localStorage
 * @param data - StorageData to save
 * @throws Error if storage fails (e.g., quota exceeded)
 */
export function saveData(data: StorageData): void {
  try {
    const json = JSON.stringify(data)
    localStorage.setItem(STORAGE_KEY, json)
  } catch (error) {
    if (error instanceof DOMException && error.name === 'QuotaExceededError') {
      throw new Error('Storage quota exceeded. Please clear some data.')
    }
    throw error
  }
}

/**
 * Validate data structure
 * @param data - Data to validate
 * @returns True if valid StorageData
 */
export function validateStorageData(data: unknown): data is StorageData {
  return validateData(data)
}

/**
 * Clear all storage data
 */
export function clearData(): void {
  localStorage.removeItem(STORAGE_KEY)
}

/**
 * Get or create default storage data
 * @returns StorageData (either loaded or empty)
 */
export function getOrCreateData(): StorageData {
  const loaded = loadData()
  if (loaded) return loaded

  const empty = createEmptyStorageData()
  saveData(empty)
  return empty
}

