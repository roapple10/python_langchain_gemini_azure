import { useState, useEffect, useCallback } from 'react'
import type { UserPreferences } from '../types/storage'
import { DEFAULT_FOCUS_DURATION_MINUTES } from '../types/storage'
import { loadData, saveData, getOrCreateData } from '../services/storage'

export interface UseUserPreferencesReturn {
  preferences: UserPreferences
  updateFocusDuration: (minutes: number) => void
  isLoading: boolean
}

export function useUserPreferences(): UseUserPreferencesReturn {
  const [preferences, setPreferences] = useState<UserPreferences>({
    focusDurationMinutes: DEFAULT_FOCUS_DURATION_MINUTES,
  })
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const data = loadData()
    if (data?.userPreferences) {
      setPreferences(data.userPreferences)
    } else {
      // Ensure default preferences are saved
      const storageData = getOrCreateData()
      if (!storageData.userPreferences) {
        storageData.userPreferences = {
          focusDurationMinutes: DEFAULT_FOCUS_DURATION_MINUTES,
        }
        saveData(storageData)
      }
      setPreferences(storageData.userPreferences)
    }
    setIsLoading(false)
  }, [])

  const updateFocusDuration = useCallback((minutes: number) => {
    if (minutes < 1 || minutes > 180 || !Number.isInteger(minutes)) {
      return
    }

    const newPreferences: UserPreferences = {
      focusDurationMinutes: minutes,
    }

    setPreferences(newPreferences)

    const data = getOrCreateData()
    data.userPreferences = newPreferences
    saveData(data)
  }, [])

  return {
    preferences,
    updateFocusDuration,
    isLoading,
  }
}

