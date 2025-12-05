import { describe, it, expect } from 'vitest'
import {
  validateSession,
  validateTree,
  validateData,
  createEmptyStorageData,
} from '../../src/utils/validation'
import type { FocusSession } from '../../src/types/session'
import type { Tree } from '../../src/types/tree'

describe('validation utilities', () => {
  describe('validateSession', () => {
    it('should validate correct session', () => {
      const session: FocusSession = {
        id: 'test-id',
        startTime: Date.now(),
        endTime: null,
        status: 'active',
        remainingSeconds: 1500,
        pausedAt: null,
        totalPausedDuration: 0,
      }

      expect(validateSession(session)).toBe(true)
    })

    it('should reject invalid session', () => {
      expect(validateSession(null)).toBe(false)
      expect(validateSession({})).toBe(false)
      expect(validateSession({ id: 'test' })).toBe(false)
    })

    it('should reject session with invalid remainingSeconds', () => {
      const session = {
        id: 'test-id',
        startTime: Date.now(),
        endTime: null,
        status: 'active',
        remainingSeconds: 2000, // > 1500
        pausedAt: null,
        totalPausedDuration: 0,
      }

      expect(validateSession(session)).toBe(false)
    })

    it('should validate paused session', () => {
      const session: FocusSession = {
        id: 'test-id',
        startTime: Date.now(),
        endTime: null,
        status: 'paused',
        remainingSeconds: 1000,
        pausedAt: Date.now(),
        totalPausedDuration: 5000,
      }

      expect(validateSession(session)).toBe(true)
    })
  })

  describe('validateTree', () => {
    it('should validate correct tree', () => {
      const tree: Tree = {
        id: 'session-id',
        completedAt: Date.now(),
        stage: 5,
        date: '2025-01-27',
      }

      expect(validateTree(tree)).toBe(true)
    })

    it('should reject invalid tree', () => {
      expect(validateTree(null)).toBe(false)
      expect(validateTree({})).toBe(false)
      expect(validateTree({ id: 'test', stage: 3 })).toBe(false) // stage must be 5
      expect(validateTree({ id: 'test', stage: 5, date: 'invalid' })).toBe(false)
    })
  })

  describe('validateData', () => {
    it('should validate correct storage data', () => {
      const data = createEmptyStorageData()
      expect(validateData(data)).toBe(true)
    })

    it('should reject invalid storage data', () => {
      expect(validateData(null)).toBe(false)
      expect(validateData({})).toBe(false)
      expect(validateData({ version: 1, sessions: [], trees: [] })).toBe(true) // missing lastActiveSessionId is ok
    })
  })

  describe('createEmptyStorageData', () => {
    it('should create valid empty storage data', () => {
      const data = createEmptyStorageData()
      expect(validateData(data)).toBe(true)
      expect(data.version).toBe(1)
      expect(data.sessions).toEqual([])
      expect(data.trees).toEqual([])
      expect(data.lastActiveSessionId).toBe(null)
    })
  })
})

