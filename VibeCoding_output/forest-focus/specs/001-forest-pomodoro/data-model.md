# Data Model: Forest-Style Pomodoro Timer

**Date**: 2025-01-27  
**Feature**: 001-forest-pomodoro

## Entities

### FocusSession

Represents a single Pomodoro timer session (active, paused, completed, or abandoned).

**Attributes**:
- `id: string` - Unique identifier (UUID v4 or timestamp-based)
- `startTime: number` - Timestamp (ms) when session started
- `endTime: number | null` - Timestamp (ms) when session ended (null if active/paused)
- `status: 'active' | 'paused' | 'completed' | 'abandoned'` - Current session state
- `remainingSeconds: number` - Remaining time in seconds (0-1500)
- `pausedAt: number | null` - Timestamp (ms) when paused (null if not paused)
- `totalPausedDuration: number` - Total milliseconds paused (for accurate timing)

**State Transitions**:
1. `null` → `active` (user starts session)
2. `active` → `paused` (user pauses)
3. `paused` → `active` (user resumes)
4. `active` | `paused` → `completed` (timer reaches 00:00)
5. `active` | `paused` → `abandoned` (user cancels)

**Validation Rules**:
- `remainingSeconds` must be between 0 and 1500 (25 minutes)
- `startTime` must be valid timestamp
- `status` must be one of the valid states
- If `status === 'paused'`, `pausedAt` must not be null
- If `status === 'completed'`, `endTime` must not be null

**Relationships**: None (sessions are independent)

---

### Tree

Represents a completed focus session saved to the user's forest.

**Attributes**:
- `id: string` - References the FocusSession id
- `completedAt: number` - Timestamp (ms) when session completed
- `stage: number` - Always 5 (mature tree stage)
- `date: string` - ISO date string (YYYY-MM-DD) for easy filtering by day

**Validation Rules**:
- `id` must reference a valid completed FocusSession
- `completedAt` must be valid timestamp
- `stage` must always be 5
- `date` must be valid ISO date string

**Relationships**: 
- Linked to FocusSession via `id` (one-to-one)

**Notes**: Only completed sessions create trees. Abandoned sessions do not create trees.

---

### ForestStats

Aggregated statistics calculated from the trees collection.

**Attributes**:
- `totalTrees: number` - Count of all completed sessions (trees.length)
- `totalFocusTimeMinutes: number` - Sum of all focus time (trees.length * 25)
- `todayCount: number` - Count of sessions completed today (local timezone)
- `dailyStreak: number` - Consecutive days with at least 1 completed session

**Calculation Logic**:
- `totalTrees`: `trees.filter(t => t.stage === 5).length`
- `totalFocusTimeMinutes`: `totalTrees * 25` (fixed 25-minute sessions)
- `todayCount`: `trees.filter(t => isToday(t.completedAt)).length`
- `dailyStreak`: Iterate backwards from today, count consecutive days with trees

**Relationships**: 
- Calculated from collection of Tree entities (derived, not stored)

**Notes**: Recalculated on-demand when trees change. Cached for performance.

---

### AppState

Current application state (not persisted, runtime only).

**Attributes**:
- `currentSession: FocusSession | null` - Currently active/paused session
- `notificationPermission: 'granted' | 'denied' | 'default'` - Browser notification permission state
- `activeTabId: string | null` - Tab identifier for multi-tab detection

**Relationships**: 
- References current FocusSession if active/paused

**Notes**: Not stored in localStorage. Reset on app load.

---

## Data Storage Schema

### localStorage Key: `forest-focus-data`

**Structure**:
```typescript
{
  version: number,           // Schema version (for migrations)
  sessions: FocusSession[],   // All sessions (for history)
  trees: Tree[],              // Completed sessions only
  lastActiveSessionId: string | null  // For multi-tab detection
}
```

**Storage Strategy**:
- Single key stores all data (simple, atomic)
- Version field allows future migrations
- Sessions array keeps history (can be pruned if needed)
- Trees array is source of truth for forest display
- `lastActiveSessionId` helps detect active sessions across tabs

**Size Considerations**:
- Each session: ~200 bytes
- Each tree: ~150 bytes
- 1000 sessions: ~200KB (well within localStorage limits ~5-10MB)
- If storage full: Show error, don't crash, allow current session to complete

---

## Data Flow

### Starting a Session
1. Create new `FocusSession` with `status: 'active'`
2. Set `startTime` to `Date.now()`
3. Set `remainingSeconds` to 1500 (25 minutes)
4. Save to localStorage `sessions` array
5. Update `AppState.currentSession`

### Pausing a Session
1. Update `FocusSession.status` to `'paused'`
2. Set `pausedAt` to `Date.now()`
3. Calculate elapsed time: `Date.now() - startTime - totalPausedDuration`
4. Update `remainingSeconds`
5. Save to localStorage

### Resuming a Session
1. Calculate pause duration: `Date.now() - pausedAt`
2. Add to `totalPausedDuration`
3. Update `status` to `'active'`
4. Clear `pausedAt`
5. Save to localStorage

### Completing a Session
1. Update `FocusSession.status` to `'completed'`
2. Set `endTime` to `Date.now()`
3. Create new `Tree` with `id` referencing session
4. Set `completedAt` to `endTime`
5. Set `stage` to 5
6. Set `date` to ISO date string
7. Add tree to `trees` array
8. Save to localStorage
9. Clear `AppState.currentSession`

### Canceling a Session
1. Update `FocusSession.status` to `'abandoned'`
2. Set `endTime` to `Date.now()`
3. Do NOT create tree
4. Save to localStorage
5. Clear `AppState.currentSession`

### Loading App State
1. Read `forest-focus-data` from localStorage
2. Validate schema (version, required fields)
3. If invalid, fallback to empty state
4. Check for paused session (`status === 'paused'`)
5. If paused session exists, restore to `AppState.currentSession`
6. Calculate `ForestStats` from `trees` array
7. Check `Notification.permission` for `AppState.notificationPermission`

---

## Validation Functions

### validateSession(session: FocusSession): boolean
- Check all required fields present
- Validate `remainingSeconds` range (0-1500)
- Validate `status` enum value
- Validate timestamps are numbers

### validateTree(tree: Tree): boolean
- Check all required fields present
- Validate `stage === 5`
- Validate `completedAt` is valid timestamp
- Validate `date` is valid ISO date string

### validateStorageData(data: any): boolean
- Check `version` field exists
- Check `sessions` is array
- Check `trees` is array
- Validate each session and tree
- Return false if any validation fails (triggers fallback)

---

## Migration Strategy

**Current Version**: 1

**Future Migrations**:
- If schema changes, increment `version`
- On load, check version
- If version mismatch, run migration function
- Migrate data to new schema
- Save with new version

**Example Migration**:
```typescript
if (data.version < 2) {
  // Migrate from v1 to v2
  data.trees = data.trees.map(tree => ({
    ...tree,
    date: new Date(tree.completedAt).toISOString().split('T')[0]
  }));
  data.version = 2;
}
```

