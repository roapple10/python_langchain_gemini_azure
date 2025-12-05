# Research: Forest-Style Pomodoro Timer

**Date**: 2025-01-27  
**Feature**: 001-forest-pomodoro

## Research Decisions

### 1. Timer Accuracy: System Time vs Interval-Based

**Decision**: Use `Date.now()` or `performance.now()` for elapsed time calculation, with `requestAnimationFrame` for UI updates.

**Rationale**: 
- `setInterval` can drift when tab is inactive or browser throttles timers
- System time (`Date.now()`) provides accurate elapsed time regardless of tab state
- `requestAnimationFrame` ensures smooth 60fps UI updates
- Calculate remaining time as: `startTime + duration - Date.now()`

**Alternatives Considered**:
- Pure `setInterval`: Rejected due to throttling in inactive tabs
- Web Workers: Rejected as unnecessary complexity for single timer
- `performance.now()`: Acceptable alternative, but `Date.now()` is simpler and sufficient

### 2. Multiple Tabs Synchronization

**Decision**: Use `localStorage` events + `BroadcastChannel` API (with fallback to storage events).

**Rationale**:
- `BroadcastChannel` provides real-time cross-tab communication
- Falls back to `storage` event listener for older browsers
- Simple implementation: one tab writes session state, others listen
- Detects active session in another tab and shows read-only view

**Alternatives Considered**:
- Service Worker: Rejected as adds complexity, not needed for simple state sync
- Polling localStorage: Rejected as inefficient and adds latency
- No sync: Rejected as violates requirement for single active session

### 3. Tree Visual Representation

**Decision**: Pure CSS animations using shapes, gradients, and transforms.

**Rationale**:
- Zero image assets = smallest bundle size
- GPU-accelerated transforms/opacity = smooth 60fps
- Scalable (works at any size)
- Easy to animate stage transitions with CSS transitions
- Aligns with <200KB bundle requirement

**Implementation Approach**:
- Stage 1 (Seed): Small circle with gradient
- Stage 2 (Sprout): Circle + small vertical line
- Stage 3 (Sapling): Trunk + few branches
- Stage 4 (Young Tree): Trunk + more branches + basic foliage
- Stage 5 (Mature Tree): Full tree with trunk, branches, dense foliage
- Use CSS `transform: scale()` and `opacity` for smooth transitions
- Use CSS custom properties (CSS variables) for stage-based styling

**Alternatives Considered**:
- SVG: Acceptable but adds ~5-10KB for tree definitions
- Image sprites: Rejected as adds 20-50KB+ to bundle
- Canvas: Rejected as requires JavaScript rendering, harder to maintain 60fps

### 4. localStorage Data Structure

**Decision**: Store sessions and trees as separate arrays with validation.

**Rationale**:
- Simple structure: `{ sessions: [], trees: [] }`
- Easy to query and filter
- Validation on load prevents corruption issues
- Can migrate schema if needed (version field)

**Data Schema**:
```typescript
{
  version: 1,
  sessions: FocusSession[],
  trees: Tree[],
  lastActiveSessionId: string | null
}
```

**Alternatives Considered**:
- IndexedDB: Rejected as overkill for simple key-value storage
- Separate keys per session: Rejected as harder to query and manage
- Single session storage: Rejected as doesn't support history

### 5. Statistics Calculation Strategy

**Decision**: Calculate stats on-demand from trees array, cache results.

**Rationale**:
- Simple: No need to maintain separate stats storage
- Accurate: Always reflects current data
- Cache results to avoid recalculating on every render
- Recalculate when trees array changes

**Calculation Approach**:
- `totalTrees`: `trees.length`
- `totalFocusTime`: `trees.length * 25` (fixed 25-minute sessions)
- `todayCount`: Filter trees by `completedAt` date (local timezone)
- `dailyStreak`: Iterate backwards from today, count consecutive days with trees

**Alternatives Considered**:
- Pre-calculated stats in storage: Rejected as adds complexity and sync issues
- Incremental updates: Rejected as YAGNI - on-demand is simpler

### 6. Browser Notification Timing

**Decision**: Request permission on first session start, show notification on completion.

**Rationale**:
- Non-blocking: App works without notifications
- User-initiated: Permission requested when user starts using feature
- Graceful degradation: App functions normally if denied

**Implementation**:
- Check `Notification.permission` on app load
- If `default`, request permission when user starts first session
- If `granted`, show notification when timer reaches 00:00
- If `denied`, silently continue (no notification)

**Alternatives Considered**:
- Request on app load: Rejected as too aggressive, may annoy users
- Never request: Rejected as violates requirement to request permission

### 7. Paused Session Recovery

**Decision**: Save paused state to localStorage, show resume option on app load.

**Rationale**:
- User control: Don't auto-resume (user may have intentionally paused)
- Clear UX: Show paused session with resume button
- Persistence: Survives browser close/refresh

**Implementation**:
- Store session with `status: 'paused'` and `remainingSeconds`
- On app load, check for paused session
- Display paused session UI with resume button
- User must explicitly click resume

**Alternatives Considered**:
- Auto-resume: Rejected as may surprise user, violates user control principle
- Discard paused sessions: Rejected as loses user progress

### 8. CSS Animation Performance

**Decision**: Use CSS transforms and opacity only, avoid layout-triggering properties.

**Rationale**:
- GPU-accelerated: `transform` and `opacity` use compositor layer
- Avoids reflow/repaint: No `width`, `height`, `top`, `left` changes
- Smooth 60fps: Browser can optimize these properties
- Use `will-change` hint for tree animations

**Best Practices**:
- Use `transform: scale()` for tree growth
- Use `opacity` for fade transitions
- Use `transition` property for smooth stage changes
- Avoid `display: none` → use `opacity: 0` + `pointer-events: none`

**Alternatives Considered**:
- JavaScript animations: Rejected as harder to maintain 60fps, adds JS overhead
- CSS animations with layout properties: Rejected as causes jank

## Technology Choices

### React + TypeScript
- **Decision**: Use React 18+ with TypeScript
- **Rationale**: Standard, well-supported, type safety, good performance
- **Alternatives**: Vanilla JS (rejected - React provides better structure), Vue (acceptable but React more common)

### Vite
- **Decision**: Use Vite 5+ as build tool
- **Rationale**: Fast dev server, optimized production builds, small config, aligns with constitution
- **Alternatives**: Webpack (rejected - slower, more config), Parcel (acceptable but Vite faster)

### Vitest
- **Decision**: Use Vitest for testing
- **Rationale**: Fast, Vite-native, TypeScript support, good React Testing Library integration
- **Alternatives**: Jest (rejected - slower, more config), Mocha (rejected - needs more setup)

### Pure CSS (No CSS-in-JS)
- **Decision**: Use CSS Modules or plain CSS files
- **Rationale**: Smaller bundle, better performance, no runtime CSS processing
- **Alternatives**: Tailwind CSS (acceptable but adds ~50KB), styled-components (rejected - runtime overhead), CSS-in-JS (rejected - bundle size)

## Performance Optimizations

1. **Code Splitting**: Lazy load forest grid if >100 trees (defer to future if needed)
2. **Tree Animation**: Use CSS `will-change: transform` for GPU hint
3. **Timer Updates**: Throttle UI updates to 1 second (timer display), use RAF for smooth animations
4. **localStorage**: Batch writes, debounce rapid updates
5. **Bundle**: Tree-shake unused code, minify production builds

## Accessibility Considerations

1. **ARIA Labels**: Add `aria-label` to timer display, tree stages, buttons
2. **Live Regions**: Use `aria-live="polite"` for timer updates
3. **Keyboard**: All buttons keyboard accessible, focus indicators visible
4. **Screen Reader**: Announce stage changes, timer completion
5. **Color Contrast**: Ensure 4.5:1 contrast for text, 3:1 for large text

## Browser Compatibility

- **Target**: Modern browsers (last 2 versions)
- **Features Used**: 
  - localStorage (IE8+)
  - Notification API (Chrome 22+, Firefox 22+, Safari 7+)
  - BroadcastChannel (Chrome 54+, Firefox 38+, Safari 15.4+)
  - CSS Grid (all modern browsers)
- **Fallbacks**: 
  - BroadcastChannel → storage events for older browsers
  - Notifications → graceful degradation if unsupported

