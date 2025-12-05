import { useState, useEffect, useRef, useCallback } from 'react'
import { calculateRemaining, isComplete } from '../services/timer'

const SESSION_DURATION_SECONDS = 1500 // 25 minutes

export interface UseTimerReturn {
  remainingSeconds: number
  isActive: boolean
  isPaused: boolean
  currentStage: number
  start: () => void
  pause: () => void
  resume: () => void
  cancel: () => void
  reset: () => void
  getStage: (seconds: number) => number
}

export function useTimer(
  durationSeconds: number = SESSION_DURATION_SECONDS,
  onComplete: () => void
): UseTimerReturn {
  const [remainingSeconds, setRemainingSeconds] = useState(durationSeconds)
  const [isActive, setIsActive] = useState(false)
  const [isPaused, setIsPaused] = useState(false)
  const [startTime, setStartTime] = useState<number | null>(null)
  const [totalPausedDuration, setTotalPausedDuration] = useState(0)
  const [pausedAt, setPausedAt] = useState<number | null>(null)

  const animationFrameRef = useRef<number>()
  const lastUpdateRef = useRef<number>(Date.now())

  // Calculate tree stage from remaining seconds proportionally
  // Stages are divided into 5 equal parts (20% each)
  // 25 minutes = baseline full growth, other durations scale proportionally
  const getStage = useCallback(
    (seconds: number): number => {
      const stageSize = durationSeconds / 5
      if (seconds >= stageSize * 4) return 1 // Stage 1: 80-100% remaining
      if (seconds >= stageSize * 3) return 2 // Stage 2: 60-80% remaining
      if (seconds >= stageSize * 2) return 3 // Stage 3: 40-60% remaining
      if (seconds >= stageSize * 1) return 4 // Stage 4: 20-40% remaining
      return 5 // Stage 5: 0-20% remaining (mature tree)
    },
    [durationSeconds]
  )

  const currentStage = getStage(remainingSeconds)

  // Update timer using requestAnimationFrame for smooth updates
  useEffect(() => {
    if (!isActive || isPaused || !startTime) {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
        animationFrameRef.current = undefined
      }
      return
    }

    const update = () => {
      const now = Date.now()
      // Update every second (1000ms) for display
      if (now - lastUpdateRef.current >= 1000) {
        const remaining = calculateRemaining(startTime, durationSeconds, totalPausedDuration)
        setRemainingSeconds(remaining)

        if (isComplete(remaining)) {
          setIsActive(false)
          setIsPaused(false)
          setStartTime(null)
          setTotalPausedDuration(0)
          setRemainingSeconds(0)
          onComplete()
          return
        }

        lastUpdateRef.current = now
      }

      animationFrameRef.current = requestAnimationFrame(update)
    }

    animationFrameRef.current = requestAnimationFrame(update)
    lastUpdateRef.current = Date.now()

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
    }
  }, [isActive, isPaused, startTime, durationSeconds, totalPausedDuration, onComplete])

  const start = useCallback(() => {
    const now = Date.now()
    setStartTime(now)
    setIsActive(true)
    setIsPaused(false)
    setTotalPausedDuration(0)
    setPausedAt(null)
    setRemainingSeconds(durationSeconds)
    lastUpdateRef.current = now
  }, [durationSeconds])

  const pause = useCallback(() => {
    if (!isActive || isPaused) return

    const now = Date.now()
    setIsPaused(true)
    setPausedAt(now)

    // Calculate elapsed pause time if resuming from previous pause
    if (startTime) {
      const elapsed = now - startTime - totalPausedDuration
      const remaining = durationSeconds * 1000 - elapsed
      setRemainingSeconds(Math.max(0, Math.floor(remaining / 1000)))
    }
  }, [isActive, isPaused, startTime, durationSeconds, totalPausedDuration])

  const resume = useCallback(() => {
    if (!isPaused || !pausedAt || !startTime) return

    const now = Date.now()
    const pauseDuration = now - pausedAt
    setTotalPausedDuration((prev) => prev + pauseDuration)
    setIsPaused(false)
    setPausedAt(null)
    lastUpdateRef.current = now
  }, [isPaused, pausedAt, startTime])

  const cancel = useCallback(() => {
    setIsActive(false)
    setIsPaused(false)
    setStartTime(null)
    setPausedAt(null)
    setTotalPausedDuration(0)
    setRemainingSeconds(durationSeconds)
  }, [durationSeconds])

  const reset = useCallback(() => {
    cancel()
  }, [cancel])

  return {
    remainingSeconds,
    isActive,
    isPaused,
    currentStage,
    start,
    pause,
    resume,
    cancel,
    reset,
    getStage,
  }
}

