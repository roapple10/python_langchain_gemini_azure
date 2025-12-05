## 1. Implementation

### 1.1 Storage & Types
- [x] 1.1.1 Add `userPreferences` field to `StorageData` type in `src/types/storage.ts`
- [x] 1.1.2 Create `UserPreferences` interface with `focusDurationMinutes` field in `src/types/storage.ts`
- [x] 1.1.3 Update `createEmptyStorageData` to include default preferences (25 minutes) in `src/utils/validation.ts`
- [x] 1.1.4 Update storage validation to handle user preferences in `src/utils/validation.ts`

### 1.2 Duration Picker Component
- [x] 1.2.1 Create `DurationPicker` component in `src/components/DurationPicker.tsx`
- [x] 1.2.2 Implement quick-select buttons for common durations (15, 25, 45, 60 minutes)
- [x] 1.2.3 Implement slider input for visual selection (range 1-180 minutes)
- [x] 1.2.4 Implement text input for precise value entry (integer only, 1-180 range)
- [x] 1.2.5 Synchronize all three inputs (buttons, slider, text input) to stay in sync
- [x] 1.2.6 Add validation for duration range (1-180 minutes, integer values only)
- [x] 1.2.7 Add accessibility attributes (ARIA labels, keyboard navigation)
- [x] 1.2.8 Style duration picker to match app design (position above start button on main screen)
- [ ] 1.2.9 Write component tests for `DurationPicker` in `tests/components/DurationPicker.test.tsx`

### 1.3 Timer Logic Updates
- [x] 1.3.1 Update `useTimer` hook to accept dynamic duration from preferences
- [x] 1.3.2 Modify `getStage` function to calculate stages proportionally based on duration (5 equal stages)
- [x] 1.3.3 Update stage calculation: divide duration into 5 equal parts instead of hardcoded intervals
- [x] 1.3.4 Update `Timer` component to remove hardcoded 1500 seconds check
- [ ] 1.3.5 Write unit tests for dynamic stage calculation in `tests/unit/useTimer.test.ts`

### 1.4 Preference Management
- [x] 1.4.1 Create `useUserPreferences` hook in `src/hooks/useUserPreferences.ts`
- [x] 1.4.2 Implement preference loading from storage
- [x] 1.4.3 Implement preference saving to storage
- [x] 1.4.4 Add default preference fallback (25 minutes)
- [ ] 1.4.5 Write unit tests for preference hook in `tests/unit/useUserPreferences.test.ts`

### 1.5 UI Integration
- [x] 1.5.1 Add duration picker to `App.tsx` on main screen, positioned above the start button
- [x] 1.5.2 Integrate `useUserPreferences` hook in `App.tsx`
- [x] 1.5.3 Pass custom duration to `useTimer` hook
- [x] 1.5.4 Update UI to show current selected duration
- [x] 1.5.5 Ensure duration picker is disabled/hidden during active sessions
- [x] 1.5.6 Ensure duration picker is NOT placed in a Settings page (main screen only)

### 1.6 Statistics Updates
- [ ] 1.6.1 Review statistics calculation logic in `src/services/storage.ts` or stats components
- [ ] 1.6.2 Ensure total focus time correctly sums variable durations
- [ ] 1.6.3 Implement Pomodoro equivalent calculation: `pomodoroCount = ceil(duration / 25.0)`
- [ ] 1.6.4 Update statistics display to show both actual time AND Pomodoro count (e.g., "45 min (≈2 🍅)")
- [ ] 1.6.5 Verify tree count and streak calculations work with variable durations
- [ ] 1.6.6 Write tests for statistics with variable durations and Pomodoro count formula

### 1.7 Testing & Validation
- [ ] 1.7.1 Write integration test for duration selection flow
- [ ] 1.7.2 Test backward compatibility (existing users get 25-minute default)
- [ ] 1.7.3 Test edge cases (1 minute, 180 minutes, invalid values)
- [ ] 1.7.4 Test preference persistence across page reloads
- [ ] 1.7.5 Verify tree stages display correctly for different durations

