## ADDED Requirements

### Requirement: Custom Focus Duration Selection
The system SHALL allow users to configure their preferred focus session duration between 1 and 180 minutes (any integer value), replacing the fixed 25-minute Pomodoro duration. The duration selector SHALL be located on the main screen above the start button, NOT in a Settings page.

#### Scenario: User selects custom duration via quick-select buttons
- **WHEN** user opens the app and no active session exists
- **THEN** quick-select buttons are displayed for common durations (15, 25, 45, 60 minutes)
- **AND** clicking a button selects that duration
- **AND** the selected duration is saved as user preference
- **AND** subsequent timer sessions use the selected duration

#### Scenario: User selects custom duration via slider
- **WHEN** user opens the app and no active session exists
- **THEN** a slider is displayed allowing selection of 1-180 minutes
- **AND** dragging the slider updates the duration value
- **AND** the slider and other inputs (buttons, text input) stay synchronized
- **AND** the selected duration is saved as user preference

#### Scenario: User selects custom duration via text input
- **WHEN** user opens the app and no active session exists
- **THEN** a text input field is displayed allowing entry of integer values (1-180)
- **AND** entering a value updates the slider and highlights matching quick-select button if applicable
- **AND** the selected duration is saved as user preference

#### Scenario: Duration preference persistence
- **WHEN** user selects a custom duration (e.g., 45 minutes)
- **THEN** the preference is saved to localStorage
- **AND** when the app is reloaded, the saved duration is restored
- **AND** new sessions default to the saved duration

#### Scenario: First visit default
- **WHEN** a user opens the app for the first time (no saved preference)
- **THEN** the default duration is 25 minutes (Pomodoro standard)
- **AND** the user can change it if desired
- **AND** subsequent visits use the user's last selected duration

#### Scenario: Duration validation
- **WHEN** user attempts to set duration outside 1-180 minute range or non-integer value
- **THEN** the system SHALL reject the invalid value
- **AND** display an appropriate error message
- **AND** maintain the previous valid duration

### Requirement: Dynamic Tree Growth Stages
The system SHALL calculate tree growth stages proportionally based on the selected focus duration. The 25-minute duration represents full growth, and all other durations scale proportionally, maintaining exactly 5 stages regardless of duration length.

#### Scenario: Proportional stage calculation for 25 minutes (baseline)
- **WHEN** user selects 25-minute duration
- **THEN** stages transition at: 20:00, 15:00, 10:00, 5:00 remaining (5-minute intervals)
- **AND** each stage represents 20% of total duration
- **AND** 25 minutes represents the full growth baseline

#### Scenario: Proportional stage calculation for custom duration (scaled)
- **WHEN** user selects 60-minute duration
- **THEN** stages transition at: 48:00, 36:00, 24:00, 12:00 remaining (12-minute intervals)
- **AND** each stage represents 20% of total duration
- **AND** visual progression scales proportionally from 25-minute baseline
- **AND** tree growth animation maintains smooth progression

#### Scenario: Minimum duration stages
- **WHEN** user selects 1-minute duration
- **THEN** stages transition at: 0:48, 0:36, 0:24, 0:12 remaining (proportional to 1 minute)
- **AND** all 5 stages are still visible and distinct
- **AND** growth scales proportionally from 25-minute baseline

### Requirement: Duration Picker UI
The system SHALL provide a user interface component for selecting focus duration on the main screen (above the start button), NOT in a Settings page. The component SHALL include quick-select buttons, slider, and text input, all synchronized and accessible.

#### Scenario: Duration picker display on main screen
- **WHEN** no active session exists
- **THEN** duration picker is visible on the main screen, positioned above the start button
- **AND** quick-select buttons (15, 25, 45, 60 min) are displayed
- **AND** slider input (1-180 minutes) is displayed
- **AND** text input for precise entry is displayed
- **AND** all three inputs show the current selected duration
- **AND** user can modify the duration using any of the three inputs

#### Scenario: Input synchronization
- **WHEN** user selects a duration using quick-select button
- **THEN** slider position updates to match the selected duration
- **AND** text input value updates to match the selected duration
- **AND** when user moves slider, text input and button highlights update accordingly
- **AND** when user types in text input, slider and button highlights update accordingly

#### Scenario: Duration picker during active session
- **WHEN** an active timer session is running
- **THEN** duration picker is disabled or hidden
- **AND** user cannot change duration mid-session

#### Scenario: Accessibility
- **WHEN** user navigates with keyboard
- **THEN** duration picker is keyboard accessible
- **AND** ARIA labels describe the duration selection
- **AND** screen readers announce the selected duration
- **AND** all interactive elements (buttons, slider, input) are keyboard navigable

### Requirement: Statistics with Variable Durations
The system SHALL correctly calculate and display statistics (total trees, focus time, streaks) regardless of session duration variations. Statistics SHALL display both actual time AND equivalent Pomodoro count using the formula: `pomodoroCount = ceil(duration / 25.0)`.

#### Scenario: Total focus time calculation with Pomodoro equivalent
- **WHEN** user completes sessions with different durations (e.g., 25 min, 45 min, 60 min)
- **THEN** total focus time accurately sums all completed session durations
- **AND** displays in appropriate time format (hours:minutes or total minutes)
- **AND** displays equivalent Pomodoro count using formula: `pomodoroCount = ceil(duration / 25.0)`
- **AND** example display format: "45 min (≈2 🍅)" or "Total: 130 min (≈5 🍅)"

#### Scenario: Individual session Pomodoro equivalent display
- **WHEN** user completes a session with duration 45 minutes
- **THEN** statistics display shows: "45 min (≈2 🍅)" where 2 = ceil(45/25.0)
- **AND** when user completes a session with duration 25 minutes
- **THEN** statistics display shows: "25 min (≈1 🍅)" where 1 = ceil(25/25.0)
- **AND** when user completes a session with duration 60 minutes
- **THEN** statistics display shows: "60 min (≈3 🍅)" where 3 = ceil(60/25.0)

#### Scenario: Tree count with variable durations
- **WHEN** user completes sessions of any duration
- **THEN** each completed session counts as one tree
- **AND** tree count is independent of session duration

#### Scenario: Daily streak with variable durations
- **WHEN** user completes at least one session of any duration per day
- **THEN** the day counts toward the daily streak
- **AND** streak calculation is independent of session duration

