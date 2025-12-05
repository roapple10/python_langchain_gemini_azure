# Tasks: Forest-Style Pomodoro Timer

**Input**: Design documents from `/specs/001-forest-pomodoro/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED - TDD is mandatory per constitution. Write tests FIRST, ensure they FAIL, then implement.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/src/`, `frontend/tests/` (per plan.md structure)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan in frontend/
- [ ] T002 Initialize Vite project with React + TypeScript template in frontend/
- [ ] T003 [P] Install dependencies: react, react-dom, typescript, vite, vitest, @testing-library/react, @testing-library/jest-dom in frontend/package.json
- [ ] T004 [P] Configure TypeScript in frontend/tsconfig.json
- [ ] T005 [P] Configure Vite build tool in frontend/vite.config.ts
- [ ] T006 [P] Configure Vitest testing framework in frontend/vitest.config.ts
- [ ] T007 [P] Setup ESLint and Prettier configuration files
- [ ] T008 Create public/index.html with proper viewport meta tag and semantic HTML structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 [P] Create FocusSession type definition in frontend/src/types/session.ts
- [ ] T010 [P] Create Tree type definition in frontend/src/types/tree.ts
- [ ] T011 [P] Create ForestStats type definition in frontend/src/types/stats.ts
- [ ] T012 [P] Create StorageData type definition in frontend/src/types/storage.ts
- [ ] T013 [P] Implement storage service with loadData, saveData, validateData functions in frontend/src/services/storage.ts
- [ ] T014 [P] Implement time formatting utility (formatTime: seconds → MM:SS) in frontend/src/utils/time.ts
- [ ] T015 [P] Implement data validation utilities (validateSession, validateTree, validateStorageData) in frontend/src/utils/validation.ts
- [ ] T016 [P] Implement timer calculation utilities (calculateRemaining, isComplete) in frontend/src/services/timer.ts
- [ ] T017 Create global CSS file with CSS custom properties, responsive breakpoints, and base styles in frontend/src/styles/global.css
- [ ] T018 [P] Write unit tests for storage service in frontend/tests/unit/storage.test.ts
- [ ] T019 [P] Write unit tests for timer utilities in frontend/tests/unit/timer.test.ts
- [ ] T020 [P] Write unit tests for validation utilities in frontend/tests/unit/validation.test.ts
- [ ] T021 [P] Write unit tests for time formatting utilities in frontend/tests/unit/time.test.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Start Timer and Watch Tree Grow (Priority: P1) 🎯 MVP

**Goal**: User can start a 25-minute Pomodoro session and see a tree visually grow through 5 distinct stages with accurate countdown timer

**Independent Test**: Start a timer session and verify: timer counts down from 25:00 to 00:00, tree progresses through 5 visual stages (seed → sprout → sapling → young tree → mature tree), each stage transition occurs at correct interval (every 5 minutes), timer displays accurate remaining time

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T022 [P] [US1] Write unit test for useTimer hook (start, countdown, stage transitions) in frontend/tests/unit/useTimer.test.ts
- [ ] T023 [P] [US1] Write component test for Timer component (displays time, shows start button) in frontend/tests/components/Timer.test.tsx
- [ ] T024 [P] [US1] Write component test for Tree component (renders 5 stages, transitions) in frontend/tests/components/Tree.test.tsx
- [ ] T025 [P] [US1] Write integration test for timer flow (start → countdown → stage transitions) in frontend/tests/integration/timer-flow.test.tsx

### Implementation for User Story 1

- [ ] T026 [P] [US1] Implement useTimer hook with accurate timing using Date.now() in frontend/src/hooks/useTimer.ts
- [ ] T027 [US1] Implement tree stage calculation logic (determine stage from remaining time) in frontend/src/hooks/useTimer.ts
- [ ] T028 [P] [US1] Create Timer component with countdown display (MM:SS format) in frontend/src/components/Timer.tsx
- [ ] T029 [P] [US1] Create Tree component with 5 CSS-based stages (seed, sprout, sapling, young tree, mature tree) in frontend/src/components/Tree.tsx
- [ ] T030 [P] [US1] Create CSS animations for tree stages using transforms and opacity in frontend/src/styles/tree.css
- [ ] T031 [US1] Implement stage transition animations (smooth 60fps transitions) in frontend/src/styles/tree.css
- [ ] T032 [US1] Create Controls component with Start button in frontend/src/components/Controls.tsx
- [ ] T033 [US1] Integrate Timer, Tree, and Controls components in App.tsx in frontend/src/App.tsx
- [ ] T034 [US1] Add ARIA labels and accessibility attributes to Timer component in frontend/src/components/Timer.tsx
- [ ] T035 [US1] Add ARIA labels and accessibility attributes to Tree component in frontend/src/components/Tree.tsx
- [ ] T036 [US1] Ensure keyboard navigation works for Start button in frontend/src/components/Controls.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently - user can start timer, see countdown, and watch tree grow through 5 stages

---

## Phase 4: User Story 2 - Pause, Resume, and Cancel Sessions (Priority: P2)

**Goal**: User can pause, resume, or cancel focus session with accurate time preservation

**Independent Test**: Start session, pause it (verify timer stops), resume it (verify continues from paused time), cancel it (verify tree killed, no save)

### Tests for User Story 2 ⚠️

- [ ] T037 [P] [US2] Write unit test for pause/resume functionality in useTimer hook in frontend/tests/unit/useTimer.test.ts
- [ ] T038 [P] [US2] Write unit test for cancel functionality in useTimer hook in frontend/tests/unit/useTimer.test.ts
- [ ] T039 [P] [US2] Write component test for pause/resume buttons in Controls component in frontend/tests/components/Controls.test.tsx
- [ ] T040 [P] [US2] Write component test for cancel button and killed tree visual feedback in frontend/tests/components/Tree.test.tsx
- [ ] T041 [P] [US2] Write integration test for pause/resume/cancel flow in frontend/tests/integration/session-controls.test.tsx

### Implementation for User Story 2

- [ ] T042 [US2] Extend useTimer hook with pause functionality (track pausedAt, totalPausedDuration) in frontend/src/hooks/useTimer.ts
- [ ] T043 [US2] Extend useTimer hook with resume functionality (calculate remaining time accurately) in frontend/src/hooks/useTimer.ts
- [ ] T044 [US2] Extend useTimer hook with cancel functionality (reset timer, mark as abandoned) in frontend/src/hooks/useTimer.ts
- [ ] T045 [US2] Update Controls component to show Pause/Resume/Cancel buttons based on session state in frontend/src/components/Controls.tsx
- [ ] T046 [US2] Implement killed tree visual feedback (fade-out animation) in frontend/src/components/Tree.tsx
- [ ] T047 [US2] Add CSS animation for killed tree state in frontend/src/styles/tree.css
- [ ] T048 [US2] Add ARIA labels for pause/resume/cancel buttons in frontend/src/components/Controls.tsx
- [ ] T049 [US2] Ensure keyboard accessibility for all control buttons in frontend/src/components/Controls.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - user can start, pause, resume, and cancel sessions

---

## Phase 5: User Story 3 - Complete Session and Save to Forest (Priority: P2)

**Goal**: Completed sessions are automatically saved to personal forest and persist across browser sessions

**Independent Test**: Complete full 25-minute session, verify mature tree appears in forest grid, verify session data persisted in localStorage, refresh page and verify forest persists

### Tests for User Story 3 ⚠️

- [ ] T050 [P] [US3] Write unit test for useSession hook (start, complete session) in frontend/tests/unit/useSession.test.ts
- [ ] T051 [P] [US3] Write unit test for useForest hook (add tree, load trees) in frontend/tests/unit/useForest.test.ts
- [ ] T052 [P] [US3] Write integration test for session completion and forest persistence in frontend/tests/integration/forest-persistence.test.tsx
- [ ] T053 [P] [US3] Write component test for ForestGrid component (displays trees) in frontend/tests/components/ForestGrid.test.tsx

### Implementation for User Story 3

- [ ] T054 [US3] Implement useSession hook with session state management and localStorage persistence in frontend/src/hooks/useSession.ts
- [ ] T055 [US3] Implement useForest hook with tree management (add, load from localStorage) in frontend/src/hooks/useForest.ts
- [ ] T056 [US3] Extend useTimer hook to call onComplete callback when timer reaches 00:00 in frontend/src/hooks/useTimer.ts
- [ ] T057 [US3] Update useSession hook to create Tree entity when session completes in frontend/src/hooks/useSession.ts
- [ ] T058 [US3] Create ForestGrid component to display saved trees in grid layout in frontend/src/components/ForestGrid.tsx
- [ ] T059 [US3] Create responsive CSS for forest grid (mobile: 2 columns, tablet: 3 columns, desktop: 4+ columns) in frontend/src/styles/forest.css
- [ ] T060 [US3] Integrate ForestGrid component into App.tsx in frontend/src/App.tsx
- [ ] T061 [US3] Implement session recovery on app load (restore paused/completed sessions) in frontend/src/hooks/useSession.ts
- [ ] T062 [US3] Add ARIA labels and accessibility attributes to ForestGrid component in frontend/src/components/ForestGrid.tsx
- [ ] T063 [US3] Handle localStorage errors gracefully (show error message, don't crash) in frontend/src/services/storage.ts

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently - user can start sessions, control them, and see completed sessions saved to forest

---

## Phase 6: User Story 4 - View Forest Grid and Statistics (Priority: P3)

**Goal**: User can see personal forest grid and statistics (total trees, total focus time, today's count, daily streak)

**Independent Test**: Complete multiple sessions on different days, verify stats calculate correctly (total trees, total time, today's count, streak), verify forest grid displays correctly

### Tests for User Story 4 ⚠️

- [ ] T064 [P] [US4] Write unit test for stats calculation utilities (totalTrees, totalFocusTime, todayCount, dailyStreak) in frontend/tests/unit/stats.test.ts
- [ ] T065 [P] [US4] Write component test for Stats component (displays all statistics) in frontend/tests/components/Stats.test.tsx
- [ ] T066 [P] [US4] Write integration test for statistics calculation from trees array in frontend/tests/integration/stats-calculation.test.tsx

### Implementation for User Story 4

- [ ] T067 [US4] Implement stats calculation service (calculateStats, isToday, calculateStreak, formatFocusTime) in frontend/src/services/stats.ts
- [ ] T068 [US4] Create Stats component to display total trees, total focus time, today's count, daily streak in frontend/src/components/Stats.tsx
- [ ] T069 [US4] Integrate Stats component into App.tsx in frontend/src/App.tsx
- [ ] T070 [US4] Style Stats component with responsive design in frontend/src/styles/global.css
- [ ] T071 [US4] Add ARIA labels and semantic HTML (dl/dt/dd) to Stats component in frontend/src/components/Stats.tsx
- [ ] T072 [US4] Ensure statistics update when new trees are added in frontend/src/components/Stats.tsx

**Checkpoint**: At this point, User Stories 1-4 should all work independently - user can see forest grid and statistics

---

## Phase 7: User Story 5 - Browser Notifications (Priority: P3)

**Goal**: User receives browser notification when focus session completes

**Independent Test**: Request notification permission, complete session and verify notification appears, handle denied permission gracefully

### Tests for User Story 5 ⚠️

- [ ] T073 [P] [US5] Write unit test for useNotifications hook (request permission, send notification) in frontend/tests/unit/useNotifications.test.ts
- [ ] T074 [P] [US5] Write component test for NotificationPrompt component in frontend/tests/components/NotificationPrompt.test.tsx
- [ ] T075 [P] [US5] Write integration test for notification flow (permission request → completion → notification) in frontend/tests/integration/notifications.test.tsx

### Implementation for User Story 5

- [ ] T076 [US5] Implement useNotifications hook with permission checking and notification sending in frontend/src/hooks/useNotifications.ts
- [ ] T077 [US5] Create NotificationPrompt component to request permission on first use in frontend/src/components/NotificationPrompt.tsx
- [ ] T078 [US5] Integrate NotificationPrompt component into App.tsx (show on first session start) in frontend/src/App.tsx
- [ ] T079 [US5] Extend useTimer hook to trigger notification on completion (if permission granted) in frontend/src/hooks/useTimer.ts
- [ ] T080 [US5] Handle browser notification API unsupported gracefully (app works without notifications) in frontend/src/hooks/useNotifications.ts
- [ ] T081 [US5] Add ARIA labels and accessibility attributes to NotificationPrompt component in frontend/src/components/NotificationPrompt.tsx

**Checkpoint**: At this point, all User Stories 1-5 should work independently - browser notifications enhance the experience but app works without them

---

## Phase 8: Multi-Tab Detection and Polish

**Purpose**: Cross-cutting concerns and final polish

- [ ] T082 Implement multi-tab detection using BroadcastChannel API (with storage event fallback) in frontend/src/hooks/useSession.ts
- [ ] T083 Show read-only view with warning message when another tab has active session in frontend/src/components/App.tsx
- [ ] T084 [P] Add comprehensive ARIA live regions for timer updates and state changes in frontend/src/components/Timer.tsx
- [ ] T085 [P] Ensure all color contrasts meet WCAG 2.1 AA standards (4.5:1 for text, 3:1 for large text) in frontend/src/styles/global.css
- [ ] T086 [P] Add focus indicators for all interactive elements in frontend/src/styles/global.css
- [ ] T087 Optimize bundle size (verify <200KB gzipped, tree-shake unused code) in frontend/vite.config.ts
- [ ] T088 [P] Add performance monitoring (measure page load time, verify <2s on 3G) in frontend/src/utils/performance.ts
- [ ] T089 [P] Verify 60fps animations (test on target device, use Chrome DevTools Performance tab) in frontend/src/styles/tree.css
- [ ] T090 Handle edge cases: localStorage full, corrupted data, system clock changes in frontend/src/services/storage.ts
- [ ] T091 Add error boundaries and graceful error handling throughout app in frontend/src/components/ErrorBoundary.tsx
- [ ] T092 [P] Run accessibility audit (keyboard navigation, screen reader testing) across all components
- [ ] T093 [P] Update documentation (README.md with setup instructions, quickstart guide validation) in frontend/README.md
- [ ] T094 Code cleanup and refactoring (remove unused code, improve naming, add comments) across codebase
- [ ] T095 Run quickstart.md validation (verify all setup steps work) in frontend/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 (extends useTimer hook)
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 (needs timer completion)
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Depends on US3 (needs trees to calculate stats)
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 (needs timer completion)

### Within Each User Story

- Tests (REQUIRED) MUST be written and FAIL before implementation
- Types before hooks
- Hooks before components
- Components before integration
- Core implementation before accessibility
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, user stories can start in parallel (with dependencies noted)
- All tests for a user story marked [P] can run in parallel
- Types within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members (respecting dependencies)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Write unit test for useTimer hook in frontend/tests/unit/useTimer.test.ts"
Task: "Write component test for Timer component in frontend/tests/components/Timer.test.tsx"
Task: "Write component test for Tree component in frontend/tests/components/Tree.test.tsx"
Task: "Write integration test for timer flow in frontend/tests/integration/timer-flow.test.tsx"

# Launch all components for User Story 1 together:
Task: "Create Timer component in frontend/src/components/Timer.tsx"
Task: "Create Tree component in frontend/src/components/Tree.tsx"
Task: "Create Controls component in frontend/src/components/Controls.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Add Polish → Final release
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (MVP)
   - Developer B: User Story 2 (can start after US1 types/hooks)
   - Developer C: User Story 3 (can start after US1)
3. After US1-3 complete:
   - Developer A: User Story 4 (depends on US3)
   - Developer B: User Story 5 (depends on US1)
   - Developer C: Polish tasks
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **CRITICAL**: Write tests FIRST, ensure they FAIL before implementation (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Test coverage target: >80% for critical paths
- Performance targets: <2s load, 60fps animations, <200KB bundle
- Accessibility: WCAG 2.1 AA compliance required

