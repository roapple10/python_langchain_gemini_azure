# Project Context

## Purpose
Forest Focus is a Pomodoro timer web application that helps users maintain focus through 25-minute work sessions. The app provides visual feedback by growing a tree during each session, creating a personal "forest" over time. Key goals include:
- Encouraging focused work through gamified Pomodoro technique
- Visual progress tracking with tree growth stages
- Statistics tracking (total trees, focus time, daily streaks)
- Offline-first experience with localStorage persistence
- Accessible, responsive design for all devices

## Tech Stack
- **Frontend Framework**: React 18.3.1 with TypeScript 5.5.3
- **Build Tool**: Vite 5.4.2
- **Testing**: Vitest 1.6.0 with Testing Library
- **Linting**: ESLint with TypeScript ESLint plugin
- **Formatting**: Prettier
- **Language**: TypeScript (ES2020 target, strict mode enabled)
- **Styling**: CSS (separate files per component/module)
- **Storage**: Browser localStorage API

## Project Conventions

### Code Style
- **Formatting**: Prettier with the following rules:
  - No semicolons
  - Single quotes for strings
  - 2-space indentation
  - Trailing commas (ES5 style)
  - Print width: 100 characters
  - Arrow function parens: avoid when possible
- **TypeScript**:
  - Strict mode enabled
  - No unused locals or parameters (prefix unused params with `_`)
  - Path aliases: `@/*` maps to `./src/*`
  - Use interfaces for type definitions
- **Naming Conventions**:
  - Components: PascalCase (e.g., `Timer.tsx`)
  - Hooks: camelCase with `use` prefix (e.g., `useTimer.ts`)
  - Utilities/services: camelCase (e.g., `time.ts`, `storage.ts`)
  - Types: PascalCase interfaces in separate files
- **File Organization**:
  - Components in `src/components/`
  - Custom hooks in `src/hooks/`
  - Business logic in `src/services/`
  - Type definitions in `src/types/`
  - Utility functions in `src/utils/`
  - Styles in `src/styles/`
  - Tests co-located or in `src/test/`

### Architecture Patterns
- **Component-Based Architecture**: React functional components with hooks
- **Separation of Concerns**:
  - Components handle UI rendering and user interactions
  - Custom hooks encapsulate stateful logic and side effects
  - Services contain pure business logic (timer calculations, storage operations)
  - Types are centralized in dedicated files
- **State Management**: React hooks (useState, useEffect, useCallback, useRef)
- **Performance Optimization**:
  - useCallback for memoizing functions passed to children
  - requestAnimationFrame for smooth timer updates
  - Manual chunk configuration for optimal bundle splitting
- **Accessibility**: ARIA labels, semantic HTML, role attributes, aria-live regions

### Testing Strategy
- **Approach**: Test-Driven Development (TDD)
  - Write tests first
  - Ensure tests fail initially
  - Implement functionality
  - Refactor while keeping tests green
- **Testing Tools**:
  - Vitest as test runner
  - jsdom for DOM simulation
  - Testing Library for React component testing
  - Jest DOM matchers for assertions
- **Coverage**:
  - V8 provider for coverage reports
  - Excludes: node_modules, test setup files, type definitions, config files
  - Run with `npm run test:coverage`
- **Test Organization**: Tests co-located with source files or in `src/test/` directory

### Git Workflow
- Standard Git workflow practices
- Commit messages should be clear and descriptive
- Use `.gitignore` to exclude:
  - Build outputs (`dist`, `build`)
  - Dependencies (`node_modules`)
  - Environment files (`.env*`)
  - Editor configs (`.vscode/*`, `.idea`)
  - Test coverage reports (`coverage`)

## Domain Context
- **Pomodoro Technique**: 25-minute focused work sessions followed by short breaks
- **Tree Growth Stages**: Visual representation of session progress
  - Stage 1 (20:00-25:00): Seed
  - Stage 2 (15:00-20:00): Sprout
  - Stage 3 (10:00-15:00): Sapling
  - Stage 4 (5:00-10:00): Young tree
  - Stage 5 (0:00-5:00): Mature tree
- **Session Management**: 
  - Default duration: 1500 seconds (25 minutes)
  - Supports pause/resume functionality
  - Tracks pause duration to maintain accurate timing
  - Cancellation resets to initial state
- **Statistics Tracking**:
  - Total completed trees
  - Total focus time
  - Daily streak counter
  - Stored in localStorage for persistence
- **Forest Visualization**: Collection of completed trees displayed as a personal forest

## Important Constraints
- **Performance Targets**:
  - Bundle size: <200KB gzipped
  - Page load: <2 seconds on 3G connection
  - Animations: 60fps smooth performance
- **Accessibility**: WCAG 2.1 AA compliance required
- **Browser Support**: Modern browsers with ES2020 support
- **Offline-First**: Must work without network connection using localStorage
- **Responsive Design**: Support for mobile, tablet, and desktop viewports
- **TypeScript**: Strict mode must remain enabled; no `any` types without justification

## External Dependencies
- **React & React DOM**: UI framework (v18.3.1)
- **Browser APIs**:
  - localStorage for data persistence
  - Notification API for browser notifications
  - requestAnimationFrame for smooth animations
- **No External Services**: Application is fully client-side with no backend dependencies
