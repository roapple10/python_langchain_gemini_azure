import { describe, it, expect, beforeEach, vi } from 'vitest'
import { calculateRemaining, isComplete } from '../../src/services/timer'

describe('timer utilities', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  describe('calculateRemaining', () => {
    it('should calculate remaining time correctly', () => {
      const startTime = Date.now()
      const durationSeconds = 1500 // 25 minutes

      // Initially, should have full duration
      expect(calculateRemaining(startTime, durationSeconds, 0)).toBe(1500)

      // After 5 seconds
      vi.advanceTimersByTime(5000)
      expect(calculateRemaining(startTime, durationSeconds, 0)).toBe(1495)

      // After 1 minute
      vi.advanceTimersByTime(55000)
      expect(calculateRemaining(startTime, durationSeconds, 0)).toBe(1440)
    })

    it('should account for paused duration', () => {
      const startTime = Date.now()
      const durationSeconds = 1500
      const pausedDuration = 60000 // 1 minute paused

      vi.advanceTimersByTime(120000) // 2 minutes elapsed

      // Should have 24 minutes remaining (25 - 2 + 1 paused)
      expect(calculateRemaining(startTime, durationSeconds, pausedDuration)).toBe(1440)
    })

    it('should not return negative values', () => {
      const startTime = Date.now() - 2000000 // Started 2000 seconds ago
      const durationSeconds = 1500

      expect(calculateRemaining(startTime, durationSeconds, 0)).toBe(0)
    })
  })

  describe('isComplete', () => {
    it('should return true when remaining is 0', () => {
      expect(isComplete(0)).toBe(true)
    })

    it('should return true when remaining is negative', () => {
      expect(isComplete(-10)).toBe(true)
    })

    it('should return false when remaining is positive', () => {
      expect(isComplete(1)).toBe(false)
      expect(isComplete(1500)).toBe(false)
    })
  })
})

