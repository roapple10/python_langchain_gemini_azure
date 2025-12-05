import { useState, useEffect, useCallback } from 'react'

interface DurationPickerProps {
  value: number
  onChange: (minutes: number) => void
  disabled?: boolean
}

const QUICK_SELECT_DURATIONS = [15, 25, 45, 60] as const
const MIN_DURATION = 1
const MAX_DURATION = 180

export function DurationPicker({ value, onChange, disabled = false }: DurationPickerProps) {
  const [textInputValue, setTextInputValue] = useState(value.toString())

  useEffect(() => {
    setTextInputValue(value.toString())
  }, [value])

  const handleQuickSelect = useCallback(
    (minutes: number) => {
      if (disabled) return
      onChange(minutes)
    },
    [onChange, disabled]
  )

  const handleSliderChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (disabled) return
      const newValue = parseInt(e.target.value, 10)
      if (!isNaN(newValue) && newValue >= MIN_DURATION && newValue <= MAX_DURATION) {
        onChange(newValue)
      }
    },
    [onChange, disabled]
  )

  const handleTextInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (disabled) return
      const inputValue = e.target.value.trim()
      setTextInputValue(inputValue)

      if (inputValue === '') return

      const numValue = parseInt(inputValue, 10)
      if (!isNaN(numValue) && numValue >= MIN_DURATION && numValue <= MAX_DURATION) {
        onChange(numValue)
      }
    },
    [onChange, disabled]
  )

  const handleTextInputBlur = useCallback(() => {
    const numValue = parseInt(textInputValue, 10)
    if (isNaN(numValue) || numValue < MIN_DURATION || numValue > MAX_DURATION) {
      setTextInputValue(value.toString())
    }
  }, [textInputValue, value])

  const handleTextInputKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter') {
        e.currentTarget.blur()
      }
    },
    []
  )

  return (
    <div className="duration-picker" aria-label="Focus duration selector">
      <div className="duration-picker-quick-select">
        <span className="sr-only">Quick select duration</span>
        {QUICK_SELECT_DURATIONS.map((minutes) => (
          <button
            key={minutes}
            type="button"
            className={`duration-btn ${value === minutes ? 'duration-btn-active' : ''}`}
            onClick={() => handleQuickSelect(minutes)}
            disabled={disabled}
            aria-label={`Select ${minutes} minutes`}
            aria-pressed={value === minutes}
          >
            {minutes} min
          </button>
        ))}
      </div>

      <div className="duration-picker-slider">
        <label htmlFor="duration-slider" className="sr-only">
          Select duration from {MIN_DURATION} to {MAX_DURATION} minutes
        </label>
        <input
          id="duration-slider"
          type="range"
          min={MIN_DURATION}
          max={MAX_DURATION}
          value={value}
          onChange={handleSliderChange}
          disabled={disabled}
          aria-label={`Duration: ${value} minutes`}
          aria-valuemin={MIN_DURATION}
          aria-valuemax={MAX_DURATION}
          aria-valuenow={value}
        />
      </div>

      <div className="duration-picker-input">
        <label htmlFor="duration-input" className="sr-only">
          Enter custom duration in minutes
        </label>
        <input
          id="duration-input"
          type="number"
          min={MIN_DURATION}
          max={MAX_DURATION}
          value={textInputValue}
          onChange={handleTextInputChange}
          onBlur={handleTextInputBlur}
          onKeyDown={handleTextInputKeyDown}
          disabled={disabled}
          aria-label={`Custom duration: ${value} minutes`}
          aria-invalid={
            parseInt(textInputValue, 10) < MIN_DURATION ||
            parseInt(textInputValue, 10) > MAX_DURATION
          }
        />
        <span className="duration-picker-unit">min</span>
      </div>
    </div>
  )
}

