# Quickstart Guide: Forest-Style Pomodoro Timer

**Date**: 2025-01-27  
**Feature**: 001-forest-pomodoro

## Overview

This guide provides a quick start for developers working on the Forest Focus Pomodoro timer application. It covers setup, key concepts, and common development tasks.

## Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Modern code editor (VS Code recommended)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Initial Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/     # React components
│   ├── hooks/         # Custom React hooks
│   ├── services/      # Business logic
│   ├── types/         # TypeScript types
│   ├── styles/        # CSS files
│   └── utils/         # Utility functions
└── tests/             # Test files
```

## Key Concepts

### Timer Accuracy

The timer uses system time (`Date.now()`) for accurate elapsed time calculation, not `setInterval`. This ensures accuracy even when the browser tab is inactive.

**Key Hook**: `useTimer.ts`
- Calculates remaining time: `startTime + duration - Date.now()`
- Updates UI via `requestAnimationFrame` for smooth 60fps
- Handles pause/resume by tracking pause duration

### Tree Visualization

Trees are rendered using pure CSS (no images) for optimal bundle size:
- 5 distinct stages (seed → sprout → sapling → young tree → mature tree)
- CSS transforms and opacity for GPU-accelerated animations
- Stage transitions every 5 minutes (at 20:00, 15:00, 10:00, 5:00 remaining)

**Key Component**: `Tree.tsx`
- Uses CSS custom properties for stage-based styling
- Animates with `transform: scale()` and `opacity`
- No image assets (keeps bundle <200KB)

### Data Persistence

All data stored in browser `localStorage`:
- Sessions history
- Completed trees (forest)
- No backend required

**Key Service**: `storage.ts`
- Abstracts localStorage operations
- Validates data on load
- Handles corruption gracefully (fallback to empty state)

### Multi-Tab Handling

Only one tab can have an active session:
- Uses `BroadcastChannel` API (with fallback to storage events)
- Other tabs detect active session and show read-only view
- Prevents conflicts and data inconsistencies

**Key Hook**: `useSession.ts`
- Manages session state
- Detects other tabs via BroadcastChannel
- Shows warning if another tab has active session

## Common Development Tasks

### Adding a New Component

1. Create component file in `src/components/`
2. Add corresponding test in `tests/components/`
3. Write test first (TDD), then implement
4. Ensure accessibility (keyboard nav, ARIA labels)

**Example**:
```typescript
// src/components/MyComponent.tsx
export function MyComponent() {
  return <div>My Component</div>;
}
```

### Adding a New Hook

1. Create hook file in `src/hooks/`
2. Add unit tests in `tests/unit/`
3. Follow React hooks rules
4. Document hook behavior

**Example**:
```typescript
// src/hooks/useMyHook.ts
export function useMyHook() {
  const [state, setState] = useState();
  return { state };
}
```

### Testing a Component

Use React Testing Library for component tests:

```typescript
import { render, screen } from '@testing-library/react';
import { Timer } from './Timer';

test('displays timer correctly', () => {
  render(<Timer remainingSeconds={1500} />);
  expect(screen.getByText('25:00')).toBeInTheDocument();
});
```

### Testing Business Logic

Use Vitest for unit tests:

```typescript
import { describe, it, expect } from 'vitest';
import { calculateStats } from './stats';

describe('calculateStats', () => {
  it('calculates total trees correctly', () => {
    const trees = [{ id: '1' }, { id: '2' }];
    const stats = calculateStats(trees);
    expect(stats.totalTrees).toBe(2);
  });
});
```

### Styling Guidelines

- Use CSS Modules or plain CSS files
- Mobile-first responsive design
- Use CSS custom properties for theming
- Avoid layout-triggering properties (use transforms/opacity)
- Ensure 60fps animations

**Example**:
```css
/* src/styles/tree.css */
.tree {
  transform: scale(var(--tree-scale));
  opacity: var(--tree-opacity);
  transition: transform 0.3s ease, opacity 0.3s ease;
}
```

## Performance Best Practices

1. **Timer Updates**: Throttle UI updates to 1 second (timer display)
2. **Animations**: Use `requestAnimationFrame` for smooth 60fps
3. **localStorage**: Batch writes, debounce rapid updates
4. **Bundle Size**: Monitor with `npm run build` (target <200KB gzipped)
5. **Tree Rendering**: Render all trees (optimize later if >1000 trees)

## Accessibility Checklist

- [ ] All interactive elements keyboard accessible
- [ ] ARIA labels on timer, tree stages, buttons
- [ ] Focus indicators visible
- [ ] Screen reader announcements for state changes
- [ ] Color contrast meets WCAG 2.1 AA (4.5:1)
- [ ] Semantic HTML (use proper elements)

## Debugging Tips

### Timer Not Accurate

- Check if using `Date.now()` for calculations (not `setInterval`)
- Verify pause duration tracking
- Check for clock changes during session

### Trees Not Saving

- Check localStorage in browser DevTools
- Verify session status is `'completed'` (not `'abandoned'`)
- Check validation errors in console

### Multi-Tab Issues

- Check BroadcastChannel support in browser
- Verify storage events are firing
- Check for localStorage conflicts

### Performance Issues

- Check bundle size: `npm run build`
- Profile animations with Chrome DevTools Performance tab
- Verify CSS animations use transforms/opacity (not layout properties)

## Testing Strategy

1. **Unit Tests**: Business logic (timer, stats, storage)
2. **Component Tests**: React components with React Testing Library
3. **Integration Tests**: Full user flows (start → pause → complete)
4. **E2E Tests**: (Future) Full app flows with Playwright/Cypress

**Run Tests**:
```bash
# Watch mode
npm test

# Coverage
npm run test:coverage

# Single file
npm test Timer.test.tsx
```

## Common Issues

### localStorage Full

- Show error message to user
- Don't crash app
- Allow current session to complete
- Suggest clearing old data

### Browser Notifications Not Working

- Check permission status
- Verify browser support
- Gracefully degrade (app works without notifications)

### Timer Drift

- Ensure using `Date.now()` not `setInterval` accumulation
- Track pause duration accurately
- Handle system clock changes

## Next Steps

1. Read `data-model.md` for entity definitions
2. Review `research.md` for technical decisions
3. Check `plan.md` for architecture overview
4. See `tasks.md` for implementation tasks (after `/speckit.tasks`)

## Resources

- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Vitest Documentation](https://vitest.dev/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

