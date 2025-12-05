# Change: Add Custom Focus Duration Feature

## Why
Currently, the Forest Focus app only supports a fixed 25-minute Pomodoro session duration. Users have different focus needs - some prefer shorter sessions (10-15 minutes) while others want longer deep work sessions (60-90 minutes). Adding custom duration support will make the app more flexible and useful for a wider range of users while maintaining the core Pomodoro experience.

## What Changes
- Add duration selector UI on main screen (above start button) with:
  - Quick-select buttons for common durations (15, 25, 45, 60 minutes)
  - Slider for visual selection (1-180 minutes)
  - Text input for precise value entry
- Store user's last selected duration in localStorage (defaults to 25 minutes on first visit)
- Update timer logic to use custom duration instead of hardcoded 25 minutes
- Recalculate tree growth stages proportionally based on selected duration (25 min = full growth, others scale proportionally)
- Update statistics display to show both actual time AND equivalent Pomodoro count using formula: `pomodoroCount = ceil(duration / 25.0)` (e.g., "45 min (≈2 🍅)")
- Duration range: 1-180 minutes, any integer value allowed (no restrictions on multiples)

## Impact
- **Affected specs**: New capability `timer-configuration` for duration settings
- **Affected code**:
  - `src/components/Timer.tsx` - Add duration picker UI
  - `src/hooks/useTimer.ts` - Use dynamic duration, recalculate stages
  - `src/types/storage.ts` - Add user preferences to storage schema
  - `src/services/storage.ts` - Handle preference loading/saving
  - `src/App.tsx` - Integrate duration picker
  - `src/types/stats.ts` - Update statistics calculations if needed
- **Breaking changes**: None (backward compatible with default 25 minutes)

