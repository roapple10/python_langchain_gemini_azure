# Feature Specification: Forest-Style Pomodoro Timer

**Feature Branch**: `001-forest-pomodoro`  
**Created**: 2025-01-27  
**Status**: Draft  
**Input**: User description: "Build a Forest-style Pomodoro app for Web: start a 25-minute session to 'plant' a tree that grows through 5 stages; cancel/quit kills the tree; completion saves it to a personal forest. Show countdown, pause/resume, browser notification, and accurate timing. Store completed/abandoned sessions locally using localStorage; show a forest grid and stats (total trees, total focus time, today's count, daily streak). Out of scope: custom durations, species, cloud sync, sharing, PWA features."

## Clarifications

### Session 2025-01-27

- Q: When user has multiple tabs open with the app, what should happen? → A: Only one tab can have active session; others show read-only view or warning message
- Q: How should trees be visually represented? → A: Pure CSS animations (shapes, gradients, transforms) - smallest bundle, GPU-accelerated

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start Timer and Watch Tree Grow (Priority: P1)

As a user, I want to start a 25-minute Pomodoro session and see a tree visually grow through 5 distinct stages, so I can stay motivated and track my focus time.

**Why this priority**: This is the core value proposition - the timer functionality and visual feedback are essential for the MVP. Without this, the app has no purpose.

**Independent Test**: Can be fully tested by starting a timer session and verifying:
- Timer counts down from 25:00 to 00:00
- Tree progresses through 5 visual stages (seed → sprout → sapling → young tree → mature tree)
- Each stage transition occurs at the correct time interval (every 5 minutes)
- Timer displays accurate remaining time

**Acceptance Scenarios**:

1. **Given** the app is loaded and no active session exists, **When** user clicks "Start Focus Session", **Then** a 25-minute timer starts counting down and tree shows stage 1 (seed)
2. **Given** a timer is running at 20:00 remaining, **When** 5 minutes elapse, **Then** tree advances to stage 2 (sprout) and timer shows 15:00
3. **Given** a timer is running at 15:00 remaining, **When** 5 minutes elapse, **Then** tree advances to stage 3 (sapling) and timer shows 10:00
4. **Given** a timer is running at 10:00 remaining, **When** 5 minutes elapse, **Then** tree advances to stage 4 (young tree) and timer shows 5:00
5. **Given** a timer is running at 5:00 remaining, **When** 5 minutes elapse, **Then** tree advances to stage 5 (mature tree) and timer shows 00:00
6. **Given** timer reaches 00:00, **When** countdown completes, **Then** session is marked as complete and tree is saved to forest

---

### User Story 2 - Pause, Resume, and Cancel Sessions (Priority: P2)

As a user, I want to pause, resume, or cancel my focus session, so I can handle interruptions without losing progress or kill sessions that I don't want to complete.

**Why this priority**: Users need control over their sessions. Pause/resume is essential for handling interruptions, and cancel is needed for sessions that shouldn't count.

**Independent Test**: Can be fully tested by:
- Starting a session, pausing it, verifying timer stops
- Resuming a paused session, verifying timer continues from where it paused
- Canceling a session, verifying tree is killed (not saved) and timer resets

**Acceptance Scenarios**:

1. **Given** a timer is running at 15:00 remaining, **When** user clicks "Pause", **Then** timer stops counting down and button changes to "Resume"
2. **Given** a timer is paused at 15:00 remaining, **When** user clicks "Resume", **Then** timer continues counting down from 15:00 and button changes to "Pause"
3. **Given** a timer is running or paused, **When** user clicks "Cancel", **Then** timer resets, tree is killed (visual feedback), session is marked as abandoned, and no tree is saved to forest
4. **Given** a timer is paused, **When** user clicks "Cancel", **Then** session is abandoned and tree is killed

---

### User Story 3 - Complete Session and Save to Forest (Priority: P2)

As a user, I want completed sessions to be automatically saved to my personal forest, so I can see my focus history and feel accomplished.

**Why this priority**: The "forest" concept is core to the app's identity. Saving completed sessions provides motivation and tracks progress.

**Independent Test**: Can be fully tested by:
- Completing a full 25-minute session
- Verifying a mature tree appears in the forest grid
- Verifying session data is persisted in localStorage
- Refreshing the page and verifying forest persists

**Acceptance Scenarios**:

1. **Given** timer reaches 00:00, **When** session completes, **Then** a mature tree is added to the forest grid and session data is saved to localStorage
2. **Given** a completed session exists in localStorage, **When** user refreshes the page, **Then** the forest grid displays all previously saved trees
3. **Given** multiple completed sessions, **When** user views the forest, **Then** trees are displayed in a grid layout showing all saved sessions
4. **Given** a session is canceled, **When** user views the forest, **Then** no tree appears for that abandoned session

---

### User Story 4 - View Forest Grid and Statistics (Priority: P3)

As a user, I want to see my personal forest grid and statistics (total trees, total focus time, today's count, daily streak), so I can track my progress and stay motivated.

**Why this priority**: Statistics provide motivation and help users track their progress over time. While important, the core timer functionality (P1) is more critical.

**Independent Test**: Can be fully tested by:
- Completing multiple sessions on different days
- Verifying stats calculate correctly (total trees, total time, today's count, streak)
- Verifying forest grid displays correctly with proper layout

**Acceptance Scenarios**:

1. **Given** user has completed 5 sessions totaling 125 minutes, **When** user views stats, **Then** total trees shows 5 and total focus time shows 125 minutes
2. **Given** user completed 2 sessions today and 1 yesterday, **When** user views stats, **Then** today's count shows 2
3. **Given** user completed at least 1 session each day for 3 consecutive days, **When** user views stats, **Then** daily streak shows 3
4. **Given** user missed a day (no sessions), **When** user views stats, **Then** daily streak resets to 0
5. **Given** user has multiple completed sessions, **When** user views forest grid, **Then** trees are displayed in a responsive grid layout (mobile: 2 columns, tablet: 3 columns, desktop: 4+ columns)

---

### User Story 5 - Browser Notifications (Priority: P3)

As a user, I want to receive a browser notification when my focus session completes, so I know when to take a break even if I'm not looking at the app.

**Why this priority**: Notifications enhance the user experience but are not essential for core functionality. The app works without them.

**Independent Test**: Can be fully tested by:
- Requesting notification permission
- Completing a session and verifying notification appears
- Handling cases where permission is denied

**Acceptance Scenarios**:

1. **Given** user has not granted notification permission, **When** user starts first session, **Then** browser prompts for notification permission
2. **Given** user has granted notification permission, **When** timer reaches 00:00, **Then** browser shows notification with message "Focus session complete! Your tree has been planted."
3. **Given** user has denied notification permission, **When** timer completes, **Then** no notification appears but session still completes normally
4. **Given** user is on a browser that doesn't support notifications, **When** timer completes, **Then** app functions normally without notification

---

### Edge Cases

- What happens when user closes the browser tab during an active session?
  - Session state should be preserved in localStorage
  - On return, user should see option to resume paused session or see completed/abandoned status
- What happens when localStorage is full or unavailable?
  - App should handle gracefully with error message
  - Should not crash or lose functionality for current session
- What happens when browser tab is inactive for extended period?
  - Timer should continue accurately using system time, not rely on active tab
  - Use Date.now() or performance.now() for accurate timing
- What happens when system clock changes during session?
  - Timer should handle clock adjustments gracefully
  - Use elapsed time calculation rather than absolute timestamps
- What happens when user has multiple tabs open with the app?
  - Only one tab can have an active session at a time
  - Other tabs detect active session in another tab and display read-only view with warning message
  - User must close other tabs or wait for session to complete before starting new session in current tab
- What happens when localStorage data is corrupted?
  - App should validate data on load
  - Fallback to empty state if data is invalid
- What happens when timer is paused and browser is closed?
  - Paused state should be saved
  - On return, user can resume from where they paused
- What happens at midnight boundary for daily streak calculation?
  - Streak should reset if no session completed on new day
  - Today's count should reset at midnight (local time)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST start a 25-minute countdown timer when user initiates a focus session
- **FR-002**: System MUST display remaining time in MM:SS format (e.g., 25:00, 15:30, 00:45)
- **FR-003**: System MUST visually represent tree growth through exactly 5 distinct stages (seed, sprout, sapling, young tree, mature tree) using pure CSS animations (shapes, gradients, transforms) for optimal bundle size and 60fps performance
- **FR-004**: System MUST transition tree to next stage every 5 minutes (at 20:00, 15:00, 10:00, 5:00 remaining)
- **FR-005**: System MUST allow user to pause an active timer session
- **FR-006**: System MUST allow user to resume a paused timer session from the exact remaining time
- **FR-007**: System MUST allow user to cancel an active or paused session
- **FR-008**: System MUST kill the tree (show visual feedback) when session is canceled
- **FR-009**: System MUST save completed sessions (mature tree) to personal forest
- **FR-010**: System MUST NOT save canceled/abandoned sessions to forest
- **FR-011**: System MUST persist all forest data and session history in localStorage
- **FR-012**: System MUST display forest grid showing all saved trees
- **FR-013**: System MUST calculate and display total trees count
- **FR-014**: System MUST calculate and display total focus time (sum of all completed 25-minute sessions)
- **FR-015**: System MUST calculate and display today's session count
- **FR-016**: System MUST calculate and display daily streak (consecutive days with at least 1 completed session)
- **FR-017**: System MUST request browser notification permission on first use
- **FR-018**: System MUST send browser notification when timer reaches 00:00
- **FR-019**: System MUST maintain accurate timing even when browser tab is inactive
- **FR-020**: System MUST handle browser tab closure gracefully (preserve session state)
- **FR-021**: System MUST use system time (Date.now() or performance.now()) for accurate timing calculations
- **FR-022**: System MUST validate localStorage data on app load and handle corruption gracefully
- **FR-023**: System MUST detect when multiple tabs are open and allow only one tab to have an active session
- **FR-024**: System MUST display read-only view with warning message in tabs that detect an active session in another tab

### Key Entities

- **FocusSession**: Represents a single Pomodoro session
  - Attributes: id (unique identifier), startTime (timestamp), endTime (timestamp or null), status (active/paused/completed/abandoned), remainingSeconds (number)
  - Relationships: None (sessions are independent)
  
- **Tree**: Represents a completed focus session saved to forest
  - Attributes: id (references FocusSession), completedAt (timestamp), stage (always 5 for mature tree)
  - Relationships: Linked to FocusSession via id
  
- **ForestStats**: Aggregated statistics about user's focus history
  - Attributes: totalTrees (count), totalFocusTimeMinutes (sum), todayCount (count for current day), dailyStreak (consecutive days)
  - Relationships: Calculated from collection of Tree entities
  
- **AppState**: Current application state
  - Attributes: currentSession (FocusSession or null), notificationPermission (granted/denied/default)
  - Relationships: References current FocusSession if active

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can start a focus session and see timer countdown accurately within 1 second of actual elapsed time
- **SC-002**: Tree stage transitions occur at correct intervals (every 5 minutes) with smooth 60fps animations
- **SC-003**: Users can pause and resume sessions without losing time accuracy (±1 second tolerance)
- **SC-004**: Completed sessions are saved to forest and persist across browser sessions (100% persistence rate)
- **SC-005**: Forest grid displays correctly on mobile (<768px), tablet (768-1024px), and desktop (>1024px) viewports
- **SC-006**: Statistics (total trees, total time, today's count, streak) calculate correctly with 100% accuracy
- **SC-007**: Browser notifications appear within 1 second of timer completion (when permission granted)
- **SC-008**: App loads in <2 seconds on 3G connection (per constitution requirement)
- **SC-009**: All animations maintain 60fps (16.67ms per frame) on target device (iPhone 6S equivalent)
- **SC-010**: Initial bundle size is <200KB gzipped (per constitution requirement)
- **SC-011**: All interactive elements are keyboard accessible (Tab navigation works for all controls)
- **SC-012**: Screen reader users can understand timer state and tree stage (proper ARIA labels)
- **SC-013**: App functions completely offline (no network requests for core functionality)
- **SC-014**: Timer accuracy maintained when browser tab is inactive for up to 25 minutes (±2 seconds tolerance)

## Out of Scope

The following features are explicitly **NOT** included in this specification:

- Custom timer durations (fixed at 25 minutes)
- Multiple tree species/varieties (single tree type)
- Cloud sync or backup functionality
- Sharing features (social media, export, etc.)
- Progressive Web App (PWA) features (installable app, service worker, offline caching beyond localStorage)
- User accounts or authentication
- Multi-device synchronization
- Custom themes or personalization beyond core functionality
- Sound effects or audio notifications (browser notifications only)
- Break timers (only focus sessions)
- Session history filtering or search
- Data export functionality

## Constitution Alignment

This specification aligns with the Forest Focus Constitution:

- **Radical Simplicity**: Fixed 25-minute duration, single tree type, no unnecessary features
- **Offline-First**: All data in localStorage, no backend or network dependencies
- **Test-First Development**: Each user story includes independent test scenarios
- **Performance Standards**: Success criteria include <2s load, 60fps animations, <200KB bundle
- **Responsive Design**: Forest grid adapts to mobile/tablet/desktop breakpoints
- **Accessibility**: Keyboard navigation and screen reader support requirements included

