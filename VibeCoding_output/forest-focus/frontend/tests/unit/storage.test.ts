import { describe, it, expect, beforeEach, vi } from 'vitest'
import {
  loadData,
  saveData,
  validateStorageData,
  clearData,
  getOrCreateData,
} from '../../src/services/storage'
import { createEmptyStorageData } from '../../src/utils/validation'
import { STORAGE_KEY } from '../../src/types/storage'

describe('storage service', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear()
  })

  describe('saveData and loadData', () => {
    it('should save and load data correctly', () => {
      const data = createEmptyStorageData()
      saveData(data)

      const loaded = loadData()
      expect(loaded).not.toBeNull()
      expect(loaded?.version).toBe(data.version)
      expect(loaded?.sessions).toEqual(data.sessions)
      expect(loaded?.trees).toEqual(data.trees)
    })

    it('should return null when no data exists', () => {
      expect(loadData()).toBeNull()
    })

    it('should return null for invalid data', () => {
      localStorage.setItem(STORAGE_KEY, 'invalid json')
      expect(loadData()).toBeNull()
    })

    it('should handle corrupted data gracefully', () => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ invalid: 'data' }))
      expect(loadData()).toBeNull()
    })
  })

  describe('validateStorageData', () => {
    it('should validate correct data', () => {
      const data = createEmptyStorageData()
      expect(validateStorageData(data)).toBe(true)
    })

    it('should reject invalid data', () => {
      expect(validateStorageData(null)).toBe(false)
      expect(validateStorageData({})).toBe(false)
    })
  })

  describe('clearData', () => {
    it('should clear storage data', () => {
      const data = createEmptyStorageData()
      saveData(data)
      expect(loadData()).not.toBeNull()

      clearData()
      expect(loadData()).toBeNull()
    })
  })

  describe('getOrCreateData', () => {
    it('should return existing data if present', () => {
      const data = createEmptyStorageData()
      data.trees = [{ id: 'test', completedAt: Date.now(), stage: 5, date: '2025-01-27' }]
      saveData(data)

      const result = getOrCreateData()
      expect(result.trees).toHaveLength(1)
    })

    it('should create and save empty data if none exists', () => {
      const result = getOrCreateData()
      expect(result).not.toBeNull()
      expect(result.version).toBe(1)
      expect(loadData()).not.toBeNull()
    })
  })

  describe('error handling', () => {
    it('should throw error when storage quota exceeded', () => {
      // Mock localStorage to throw QuotaExceededError
      const originalSetItem = localStorage.setItem
      localStorage.setItem = vi.fn(() => {
        const error = new DOMException('Quota exceeded', 'QuotaExceededError')
        throw error
      })

      const data = createEmptyStorageData()
      expect(() => saveData(data)).toThrow('Storage quota exceeded')

      localStorage.setItem = originalSetItem
    })
  })
})

