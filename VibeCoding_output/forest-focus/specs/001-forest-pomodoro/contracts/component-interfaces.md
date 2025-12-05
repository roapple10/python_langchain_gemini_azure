# Component Interfaces: Forest-Style Pomodoro Timer

**Date**: 2025-01-27  
**Feature**: 001-forest-pomodoro

## Overview

Since this is a frontend-only application with no backend API, contracts are defined as TypeScript interfaces for React components and hooks. These serve as the "API contracts" between components.

## Component Contracts

### Timer Component

**File**: `src/components/Timer.tsx`

**Props**:
```typescript
interface TimerProps {
  remainingSeconds: number;        // 0-1500
  isPaused: boolean;                // Timer pause state
  onPause: () => void;              // Pause callback
  onResume: () => void;             // Resume callback
  onCancel: () => void;              // Cancel callback
  onStart: () => void;               // Start callback
}
```

**Behavior**:
- Displays time in MM:SS format (e.g., "25:00", "15:30", "00:45")
- Shows appropriate button based on state (Start/Pause/Resume/Cancel)
- Updates display every second when active
- Accessible via keyboard (Tab navigation, Enter/Space to activate)

**Accessibility**:
- `aria-label`: "Timer: {minutes} minutes {seconds} seconds remaining"
- `aria-live="polite"`: Announces time updates
- Keyboard: Tab to buttons, Enter/Space to activate

---

### Tree Component

**File**: `src/components/Tree.tsx`

**Props**:
```typescript
interface TreeProps {
  stage: 1 | 2 | 3 | 4 | 5;         // Current growth stage
  isKilled?: boolean;                // Show killed tree animation
  size?: 'small' | 'medium' | 'large'; // Size variant (for forest grid)
}
```

**Behavior**:
- Renders tree visualization using pure CSS
- Animates stage transitions smoothly (60fps)
- Shows killed state with fade-out animation if `isKilled` is true
- Responsive sizing based on `size` prop

**Accessibility**:
- `aria-label`: "Tree stage {stage}: {stageName}"
- `role="img"`: Indicates decorative image
- Screen reader announces stage changes

**CSS Classes**:
- `.tree-stage-1` through `.tree-stage-5`: Stage-specific styling
- `.tree-killed`: Killed tree animation
- `.tree-small`, `.tree-medium`, `.tree-large`: Size variants

---

### ForestGrid Component

**File**: `src/components/ForestGrid.tsx`

**Props**:
```typescript
interface ForestGridProps {
  trees: Tree[];                    // Array of completed trees
  columns?: number;                   // Grid columns (auto-calculated if not provided)
}
```

**Behavior**:
- Displays trees in responsive grid layout
- Mobile: 2 columns, Tablet: 3 columns, Desktop: 4+ columns
- Shows empty state if no trees
- Lazy renders trees (optimize if >100 trees)

**Accessibility**:
- `aria-label`: "Forest: {count} trees planted"
- `role="grid"`: Grid structure
- Keyboard navigation: Arrow keys navigate grid (optional enhancement)

---

### Stats Component

**File**: `src/components/Stats.tsx`

**Props**:
```typescript
interface StatsProps {
  stats: ForestStats;                 // Calculated statistics
}
```

**Behavior**:
- Displays total trees, total focus time, today's count, daily streak
- Formats time as "X hours Y minutes" or "X minutes"
- Updates when stats change
- Shows empty state if no stats

**Accessibility**:
- Semantic HTML: `<dl>` for definition list
- `aria-label` on each stat item
- Screen reader announces stat values

---

### Controls Component

**File**: `src/components/Controls.tsx`

**Props**:
```typescript
interface ControlsProps {
  session: FocusSession | null;      // Current session state
  onStart: () => void;                // Start session callback
  onPause: () => void;                // Pause session callback
  onResume: () => void;               // Resume session callback
  onCancel: () => void;               // Cancel session callback
}
```

**Behavior**:
- Shows appropriate buttons based on session state
- Disables buttons when appropriate (e.g., no cancel during completion)
- Keyboard accessible (Tab navigation)

**Button States**:
- No session: Show "Start Focus Session"
- Active session: Show "Pause" and "Cancel"
- Paused session: Show "Resume" and "Cancel"
- Completing: Disable all buttons

**Accessibility**:
- `aria-label` on each button
- Focus indicators visible
- Keyboard: Tab to navigate, Enter/Space to activate

---

### NotificationPrompt Component

**File**: `src/components/NotificationPrompt.tsx`

**Props**:
```typescript
interface NotificationPromptProps {
  permission: 'default' | 'granted' | 'denied';
  onRequest: () => void;              // Request permission callback
}
```

**Behavior**:
- Shows prompt only if `permission === 'default'`
- Requests notification permission when user clicks
- Hides after permission granted/denied
- Non-blocking (app works without notifications)

**Accessibility**:
- `aria-label`: "Request browser notification permission"
- Clear button text: "Enable Notifications"

---

## Hook Contracts

### useTimer Hook

**File**: `src/hooks/useTimer.ts`

**Signature**:
```typescript
function useTimer(
  durationSeconds: number,           // Timer duration (1500 for 25 minutes)
  onComplete: () => void             // Completion callback
): {
  remainingSeconds: number;           // Current remaining time
  isActive: boolean;                  // Timer is running
  isPaused: boolean;                  // Timer is paused
  start: () => void;                  // Start timer
  pause: () => void;                  // Pause timer
  resume: () => void;                 // Resume timer
  cancel: () => void;                 // Cancel timer
  reset: () => void;                  // Reset timer
}
```

**Behavior**:
- Uses `Date.now()` for accurate timing
- Updates remaining time every second
- Handles pause/resume correctly
- Calls `onComplete` when timer reaches 0
- Maintains accuracy when tab inactive

---

### useSession Hook

**File**: `src/hooks/useSession.ts`

**Signature**:
```typescript
function useSession(): {
  session: FocusSession | null;       // Current session
  startSession: () => void;           // Start new session
  pauseSession: () => void;           // Pause current session
  resumeSession: () => void;          // Resume paused session
  cancelSession: () => void;          // Cancel current session
  completeSession: () => void;        // Mark session as complete
  isLoading: boolean;                 // Loading state
}
```

**Behavior**:
- Manages session state in localStorage
- Detects multi-tab conflicts
- Handles session recovery on app load
- Persists session state across page reloads

---

### useForest Hook

**File**: `src/hooks/useForest.ts`

**Signature**:
```typescript
function useForest(): {
  trees: Tree[];                      // All saved trees
  addTree: (tree: Tree) => void;      // Add completed tree
  clearForest: () => void;            // Clear all trees (optional)
  isLoading: boolean;                 // Loading state
}
```

**Behavior**:
- Loads trees from localStorage
- Validates tree data on load
- Handles corruption gracefully
- Updates trees array when new tree added

---

### useNotifications Hook

**File**: `src/hooks/useNotifications.ts`

**Signature**:
```typescript
function useNotifications(): {
  permission: 'default' | 'granted' | 'denied';
  requestPermission: () => Promise<void>;
  notify: (message: string) => void;   // Send notification
}
```

**Behavior**:
- Checks browser notification support
- Requests permission when needed
- Sends notification if permission granted
- Gracefully degrades if unsupported

---

## Service Contracts

### Storage Service

**File**: `src/services/storage.ts`

**Exports**:
```typescript
// Load data from localStorage
function loadData(): StorageData | null;

// Save data to localStorage
function saveData(data: StorageData): void;

// Validate data structure
function validateData(data: any): data is StorageData;

// Clear all data
function clearData(): void;
```

**Types**:
```typescript
interface StorageData {
  version: number;
  sessions: FocusSession[];
  trees: Tree[];
  lastActiveSessionId: string | null;
}
```

**Behavior**:
- Handles localStorage errors gracefully
- Validates data on load
- Falls back to empty state if corrupted
- Throws errors if storage full (caller handles)

---

### Timer Service

**File**: `src/services/timer.ts`

**Exports**:
```typescript
// Format seconds to MM:SS string
function formatTime(seconds: number): string;

// Calculate remaining time from start time
function calculateRemaining(
  startTime: number,
  durationSeconds: number,
  totalPausedDuration: number
): number;

// Check if timer is complete
function isComplete(remainingSeconds: number): boolean;
```

---

### Stats Service

**File**: `src/services/stats.ts`

**Exports**:
```typescript
// Calculate statistics from trees
function calculateStats(trees: Tree[]): ForestStats;

// Check if date is today (local timezone)
function isToday(timestamp: number): boolean;

// Calculate daily streak from trees
function calculateStreak(trees: Tree[]): number;

// Format focus time as human-readable string
function formatFocusTime(minutes: number): string;
```

---

## Type Definitions

**File**: `src/types/session.ts`

```typescript
export interface FocusSession {
  id: string;
  startTime: number;
  endTime: number | null;
  status: 'active' | 'paused' | 'completed' | 'abandoned';
  remainingSeconds: number;
  pausedAt: number | null;
  totalPausedDuration: number;
}
```

**File**: `src/types/tree.ts`

```typescript
export interface Tree {
  id: string;
  completedAt: number;
  stage: 5;
  date: string; // ISO date string (YYYY-MM-DD)
}
```

**File**: `src/types/stats.ts`

```typescript
export interface ForestStats {
  totalTrees: number;
  totalFocusTimeMinutes: number;
  todayCount: number;
  dailyStreak: number;
}
```

---

## Contract Testing

These interfaces serve as contracts for:
1. **Component Testing**: Verify components accept correct props
2. **Hook Testing**: Verify hooks return expected shape
3. **Integration Testing**: Verify components work together correctly
4. **Type Safety**: TypeScript enforces contracts at compile time

**Example Contract Test**:
```typescript
import { Timer } from './Timer';

test('Timer accepts correct props', () => {
  const props = {
    remainingSeconds: 1500,
    isPaused: false,
    onPause: jest.fn(),
    onResume: jest.fn(),
    onCancel: jest.fn(),
    onStart: jest.fn(),
  };
  
  render(<Timer {...props} />);
  // Component should render without errors
});
```

