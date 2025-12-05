import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { renderHook, act, waitFor } from '@testing-library/react'
import { useTimer } from '../../src/hooks/useTimer'

describe('useTimer hook', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('should initialize with correct default values', () => {
    const { result } = renderHook(() => useTimer(1500, vi.fn()))

    expect(result.current.remainingSeconds).toBe(1500)
    expect(result.current.isActive).toBe(false)
    expect(result.current.isPaused).toBe(false)
  })

  it('should start timer and countdown', async () => {
    const onComplete = vi.fn()
    const { result } = renderHook(() => useTimer(1500, onComplete))

    act(() => {
      result.current.start()
    })

    expect(result.current.isActive).toBe(true)
    expect(result.current.remainingSeconds).toBe(1500)

    // Advance time by 1 second
    act(() => {
      vi.advanceTimersByTime(1000)
    })

    await waitFor(() => {
      expect(result.current.remainingSeconds).toBeLessThan(1500)
    })
  })

  it('should calculate tree stage correctly', () => {
    const { result } = renderHook(() => useTimer(1500, vi.fn()))

    // Stage 1: 20:00 - 25:00 (1500 - 1200 seconds)
    expect(result.current.getStage(1500)).toBe(1)
    expect(result.current.getStage(1200)).toBe(1)

    // Stage 2: 15:00 - 20:00 (1200 - 900 seconds)
    expect(result.current.getStage(1199)).toBe(2)
    expect(result.current.getStage(900)).toBe(2)

    // Stage 3: 10:00 - 15:00 (900 - 600 seconds)
    expect(result.current.getStage(899)).toBe(3)
    expect(result.current.getStage(600)).toBe(3)

    // Stage 4: 5:00 - 10:00 (600 - 300 seconds)
    expect(result.current.getStage(599)).toBe(4)
    expect(result.current.getStage(300)).toBe(4)

    // Stage 5: 0:00 - 5:00 (300 - 0 seconds)
    expect(result.current.getStage(299)).toBe(5)
    expect(result.current.getStage(0)).toBe(5)
  })

  it('should call onComplete when timer reaches 0', async () => {
    const onComplete = vi.fn()
    const { result } = renderHook(() => useTimer(5, onComplete)) // 5 seconds for testing

    act(() => {
      result.current.start()
    })

    act(() => {
      vi.advanceTimersByTime(5000)
    })

    await waitFor(() => {
      expect(onComplete).toHaveBeenCalled()
      expect(result.current.remainingSeconds).toBe(0)
    })
  })
})

