import { describe, it, expect } from 'vitest'
import { formatTime } from '../../src/utils/time'

describe('formatTime', () => {
  it('should format seconds to MM:SS', () => {
    expect(formatTime(0)).toBe('00:00')
    expect(formatTime(45)).toBe('00:45')
    expect(formatTime(60)).toBe('01:00')
    expect(formatTime(1500)).toBe('25:00')
    expect(formatTime(3661)).toBe('61:01')
  })

  it('should handle edge cases', () => {
    expect(formatTime(-10)).toBe('00:00')
    expect(formatTime(3600)).toBe('60:00')
    expect(formatTime(5000)).toBe('60:00') // Clamped to 60:00
  })

  it('should pad single digits with zeros', () => {
    expect(formatTime(5)).toBe('00:05')
    expect(formatTime(65)).toBe('01:05')
    expect(formatTime(305)).toBe('05:05')
  })
})

